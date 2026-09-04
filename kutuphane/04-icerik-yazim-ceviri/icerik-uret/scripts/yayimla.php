<?php
/**
 * Üç dilli kayıt yayımlayıcı.
 *
 * Kullanım (konteyner içinde):
 *   wp eval-file /tools/yayimla.php /tools/icerik.json --allow-root
 *
 * JSON tek bir kaydı üç dilde tanımlar (bkz. ornek-icerik.json). Betik:
 *   - üç kaydı açar ya da mevcutları günceller (slug + dil ile eşleşir)
 *   - dilleri atar ve çeviri bağını kurar
 *   - sayısal alanları ve görsel kimliklerini üç dile kopyalar
 *   - `city` ve `stops` ilişkilerini HER DİLDE o dilin kaydına eşler
 *
 * Aynı dosya ikinci kez çalıştırılırsa kopya üretmez, günceller.
 */

$path = $args[0] ?? '';
if ( ! $path || ! file_exists( $path ) ) {
	WP_CLI::error( "JSON bulunamadı: $path" );
}

$doc = json_decode( file_get_contents( $path ), true );
if ( ! is_array( $doc ) ) {
	WP_CLI::error( 'JSON çözümlenemedi: ' . json_last_error_msg() );
}

$type = $doc['type'] ?? '';
if ( ! in_array( $type, array( 'city', 'place', 'route' ), true ) ) {
	WP_CLI::error( "Geçersiz tip: '$type'. Beklenen: city, place, route." );
}

$diller = array( 'tr', 'en', 'ar' );

foreach ( $diller as $lang ) {
	if ( empty( $doc[ $lang ] ) ) {
		WP_CLI::error( "'$lang' bloğu eksik. Bir kayıt üç dilde birden yayımlanır." );
	}
}

/**
 * Bir kaydın hedef dildeki karşılığı.
 *
 * İlişkiler elle eşlenmez; çeviri kümesinden okunur. Kimlikler yayımlama
 * sırasına göre değiştiği için elle yazılan her kimlik er geç yanlışa dönüyor.
 */
function cs_hedef( int $id, string $lang ): ?int {
	if ( $id <= 0 ) {
		return null;
	}
	$set = pll_get_post_translations( $id );

	return isset( $set[ $lang ] ) ? (int) $set[ $lang ] : null;
}

/**
 * Bir slug'ı belirli bir dilde arar.
 *
 * `stops` ve `city` alanları JSON'da **Türkçe slug** ile yazılıyor — kimlik
 * yazmak kırılgan. Betik bunu önce Türkçe kayda, oradan hedef dile çözüyor.
 */
function cs_slug_to_id( string $slug, string $post_type, string $lang = 'tr' ): ?int {
	$found = get_posts(
		array(
			'post_type'   => $post_type,
			'name'        => $slug,
			'post_status' => array( 'publish', 'draft' ),
			'numberposts' => 1,
			'lang'        => $lang,
		)
	);

	return $found ? (int) $found[0]->ID : null;
}

$ortak    = (array) ( $doc['ortak'] ?? array() );
$kimlikler = array();
$uyari    = 0;

// --- 1. Geçiş: kayıtları aç ve dilleri ata --------------------------------

foreach ( $diller as $lang ) {
	$blok = $doc[ $lang ];

	$mevcut = get_posts(
		array(
			'post_type'   => $type,
			'name'        => $blok['slug'],
			'post_status' => array( 'publish', 'draft' ),
			'numberposts' => 1,
			'lang'        => $lang,
		)
	);

	$data = array(
		'post_type'    => $type,
		'post_status'  => $doc['status'] ?? 'publish',
		'post_name'    => $blok['slug'],
		'post_title'   => $blok['title'],
		'post_excerpt' => $blok['excerpt'],
		'post_content' => $blok['content'],
	);

	if ( $mevcut ) {
		$data['ID'] = $mevcut[0]->ID;
		$id         = wp_update_post( $data, true );
	} else {
		$id = wp_insert_post( $data, true );
	}

	if ( is_wp_error( $id ) ) {
		WP_CLI::error( "[$lang] {$blok['slug']}: " . $id->get_error_message() );
	}

	pll_set_post_language( $id, $lang );
	$kimlikler[ $lang ] = (int) $id;

	// Dile özgü alanlar.
	foreach ( (array) ( $blok['fields'] ?? array() ) as $key => $value ) {
		if ( $value === null || $value === '' || $value === array() ) {
			delete_post_meta( $id, 'cs_' . $key );
		} else {
			update_post_meta( $id, 'cs_' . $key, $value );
		}
	}

	// Üç dilde ortak sayısal alanlar.
	foreach ( $ortak as $key => $value ) {
		if ( $value !== null && $value !== '' ) {
			update_post_meta( $id, 'cs_' . $key, $value );
		}
	}

	// Görseller: aynı ek kimliği. Polylang'de medya çevirisi kapalı olduğu için
	// bir ek bütün dillerde ortak ve aynı kimlik aynı dosyayı veriyor.
	if ( ! empty( $doc['featured_media'] ) ) {
		set_post_thumbnail( $id, (int) $doc['featured_media'] );
	}
	if ( ! empty( $doc['gallery'] ) ) {
		update_post_meta( $id, 'cs_gallery', array_map( 'intval', $doc['gallery'] ) );
	}
}

// --- 2. Çeviri bağı -------------------------------------------------------

pll_save_post_translations( $kimlikler );

// --- 3. İlişkileri her dilde o dilin kaydına eşle -------------------------

foreach ( $diller as $lang ) {
	$id = $kimlikler[ $lang ];

	if ( ! empty( $doc['city'] ) ) {
		$tr_sehir = cs_slug_to_id( (string) $doc['city'], 'city' );
		if ( ! $tr_sehir ) {
			WP_CLI::warning( "  şehir slug'ı bulunamadı: {$doc['city']}" );
			$uyari++;
		} else {
			$hedef = cs_hedef( $tr_sehir, $lang );
			if ( $hedef ) {
				update_post_meta( $id, 'cs_city', $hedef );
			} else {
				WP_CLI::warning( "  [$lang] şehir '{$doc['city']}' bu dilde henüz yok" );
				$uyari++;
			}
		}
	}

	if ( ! empty( $doc['stops'] ) ) {
		$duraklar = array();
		foreach ( (array) $doc['stops'] as $i => $durak ) {
			$tr_mekan = cs_slug_to_id( (string) $durak['place'], 'place' );
			if ( ! $tr_mekan ) {
				WP_CLI::warning( "  durak slug'ı bulunamadı: {$durak['place']}" );
				$uyari++;
				continue;
			}
			$hedef = cs_hedef( $tr_mekan, $lang );
			if ( ! $hedef ) {
				WP_CLI::warning( "  [$lang] durak '{$durak['place']}' bu dilde henüz yok" );
				$uyari++;
				continue;
			}
			$duraklar[] = array(
				'place' => $hedef,
				'note'  => (string) ( $doc[ $lang ]['stop_notes'][ $i ] ?? $durak['note'] ?? '' ),
			);
		}
		update_post_meta( $id, 'cs_stops', $duraklar );
	}
}

foreach ( $diller as $lang ) {
	WP_CLI::log(
		sprintf(
			'%-3s %-34s id=%-4d kapak=%s',
			$lang,
			$doc[ $lang ]['slug'],
			$kimlikler[ $lang ],
			$doc['featured_media'] ?? '-'
		)
	);
}

if ( $uyari ) {
	WP_CLI::warning( "$uyari ilişki eşlenemedi — bağlı kaydı önce yayımlayıp betiği tekrar çalıştır." );
}

WP_CLI::success( "$type üç dilde yayımlandı." );
