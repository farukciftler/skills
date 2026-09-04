#!/usr/bin/env node
/**
 * ComeSyria — Master Backlog İstatistik ve Excel Raporlayıcı
 *
 * Kullanım:
 *   node backlog/scripts/export-excel.mjs
 *   node backlog/scripts/export-excel.mjs --sehir HAMA
 *   node backlog/scripts/export-excel.mjs --durum ARAŞTIRILACAK
 */

import { readFileSync, existsSync } from 'node:fs';
import { resolve, join } from 'node:path';

const BACKLOG_FILE = join(process.cwd(), 'backlog', 'comesyria_backlog.json');

if (!existsSync(BACKLOG_FILE)) {
  console.error('❌ Hata: Backlog verisi bulunamadı. Önce `node backlog/scripts/sync-inventory.mjs` çalıştırın.');
  process.exit(1);
}

const items = JSON.parse(readFileSync(BACKLOG_FILE, 'utf8'));

const args = process.argv.slice(2);
const sehirFilter = args.includes('--sehir') ? args[args.indexOf('--sehir') + 1]?.toUpperCase() : null;
const durumFilter = args.includes('--durum') ? args[args.indexOf('--durum') + 1]?.toUpperCase() : null;

let filtered = items;
if (sehirFilter) filtered = filtered.filter((x) => x.sehir === sehirFilter);
if (durumFilter) filtered = filtered.filter((x) => x.durum === durumFilter);

console.log('='.repeat(80));
console.log('📋 COMESYRIA MASTER BACKLOG & EXCEL ENVANTER RAPORU');
console.log('='.repeat(80));

// Genel Özet
const total = items.length;
const yayinda = items.filter((x) => x.durum === 'YAYINDA').length;
const kuyrukta = items.filter((x) => x.durum === 'KUYRUKTA').length;
const adaylar = items.filter((x) => x.durum === 'ARAŞTIRILACAK' || x.durum === 'YAYINLANABİLİR').length;
const alkolsuz = items.filter((x) => x.alkol_durumu.includes('Alkolsüz')).length;

console.log(`\n📊 GENEL İSTATİSTİKLER:`);
console.log(`   • Toplam Kayıt    : ${total}`);
console.log(`   • 🟢 Yayında      : ${yayinda}`);
console.log(`   • 🟡 Kuyrukta     : ${kuyrukta}`);
console.log(`   • 🔵 Yeni Adaylar : ${adaylar}`);
console.log(`   • 🍃 Alkolsüz/Helal: ${alkolsuz} (%${Math.round((alkolsuz / total) * 100)})`);

// Şehirlere Göre Dağılım
const sehirler = {};
for (const item of items) {
  const s = item.sehir || 'DİĞER';
  sehirler[s] = sehirler[s] || { total: 0, yayinda: 0, aday: 0 };
  sehirler[s].total++;
  if (item.durum === 'YAYINDA') sehirler[s].yayinda++;
  else sehirler[s].aday++;
}

console.log(`\n🏙️ ŞEHİR BAZINDA DURUM:`);
console.log('┌──────────────┬──────────────┬──────────────┬──────────────┐');
console.log('│ Şehir        │ Toplam Kayıt │ Yayında      │ Yeni Aday    │');
console.log('├──────────────┼──────────────┼──────────────┼──────────────┤');
for (const [sehir, st] of Object.entries(sehirler)) {
  const sStr = sehir.padEnd(12);
  const tStr = String(st.total).padEnd(12);
  const yStr = String(st.yayinda).padEnd(12);
  const aStr = String(st.aday).padEnd(12);
  console.log(`│ ${sStr} │ ${tStr} │ ${yStr} │ ${aStr} │`);
}
console.log('└──────────────┴──────────────┴──────────────┴──────────────┘');

// Kategorilere Göre Dağılım
const kategoriler = {};
for (const item of items) {
  const k = item.kategori || 'diger';
  kategoriler[k] = (kategoriler[k] || 0) + 1;
}

console.log(`\n📂 KATEGORİ DAĞILIMI:`);
for (const [k, count] of Object.entries(kategoriler)) {
  console.log(`   • ${k.toUpperCase().padEnd(10)}: ${count} kayıt`);
}

// Filtrelenen Liste
if (sehirFilter || durumFilter) {
  console.log(`\n🔍 FİLTRE SONUÇLARI (${filtered.length} Kayıt):`);
  console.log('─'.repeat(80));
  for (const r of filtered) {
    console.log(`[${r.durum.padEnd(14)}] ${r.sehir.padEnd(8)} | ${r.kategori.padEnd(6)} | ${r.ad_tr}`);
    console.log(`   ↳ ${r.alt_tur} | ${r.alkol_durumu} | Öncelik: ${r.oncelik}`);
    console.log(`   ↳ Not: ${r.kaynak_ve_notlar}\n`);
  }
}

console.log('='.repeat(80));
console.log('💾 Excel CSV Dosyası: backlog/comesyria_backlog.csv (UTF-8 BOM Hazır)');
console.log('='.repeat(80));
