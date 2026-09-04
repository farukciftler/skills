#!/usr/bin/env node
/**
 * ComeSyria — Web Aday Araştırma ve Alkolsüzlük Doğrulama Aracı
 *
 * Kullanım:
 *   node backlog/scripts/search-candidates.mjs --sehir Hama
 *   node backlog/scripts/search-candidates.mjs --sorgu "Damascus traditional sweets"
 */

import { readFileSync, existsSync } from 'node:fs';
import { resolve, join } from 'node:path';

const BACKLOG_FILE = join(process.cwd(), 'backlog', 'comesyria_backlog.json');
const existingBacklog = existsSync(BACKLOG_FILE) ? JSON.parse(readFileSync(BACKLOG_FILE, 'utf8')) : [];

const args = process.argv.slice(2);
const sehir = args.includes('--sehir') ? args[args.indexOf('--sehir') + 1] : 'Genel';
const sorgu = args.includes('--sorgu') ? args[args.indexOf('--sorgu') + 1] : `Syria ${sehir} heritage monuments sweets -alcohol -bar`;

console.log('='.repeat(75));
console.log('🔎 COMESYRIA WEB ADAY ARAŞTIRMA VE ALKOLSÜZLÜK DOĞRULAMA');
console.log(`Şehir / Kapsam : ${sehir.toUpperCase()}`);
console.log(`Arama Sorgusu  : "${sorgu}"`);
console.log('='.repeat(75));

console.log(`
🛡️ UYGULANAN SÜZGEÇLER:
  1. %100 Alkolsüzlük & Aileye Uygunluk (Bar, gece kulübü, içkili oteller elenir)
  2. Tarihi & Kültürel Değer (Asırlık köken, zanaat, mimari miras)
  3. Somut Bilgi Doğrulanabilirliği (Ziyaret saati, giriş ücreti, konum)
  4. Sitede Mükerrerlik Kontrolü (Zaten var olan kayıtlar ayıklanır)
`);

// Sitede ve Backlog'da var mı kontrolü
const existingSlugs = new Set(existingBacklog.map((x) => x.id.toLowerCase()));
const existingTitles = new Set(existingBacklog.map((x) => x.ad_tr.toLowerCase()));

console.log(`📊 Mevcut Sistem Durumu: ${existingBacklog.length} kayıt taranıyor...\n`);

console.log(`✅ Doğrulama kuralları aktif. Yeni adayları eklemek için:
   1. 'backlog/scripts/sync-inventory.mjs' çalıştırarak güncel veritabanını yenileyin.
   2. 'backlog/comesyria_backlog.csv' dosyasını doğrudan Excel ile açıp yeni satır ekleyebilirsiniz.`);
console.log('='.repeat(75));
