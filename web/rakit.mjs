// Merakit desain web/desain/*.dc.html menjadi halaman HTML statis di _site/.
// Dijalankan oleh Netlify saat deploy: `node web/rakit.mjs`.
import { readFileSync, writeFileSync, mkdirSync, rmSync, readdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import vm from 'node:vm';

const akar = dirname(fileURLToPath(import.meta.url));
const sumber = join(akar, 'desain');
const keluaran = join(akar, '..', '_site');

// Nama berkas desain -> alamat halaman di situs
const alamat = {
  'Main.dc.html': 'index.html',
  'Kerja.dc.html': 'kerja.html',
  'Firma.dc.html': 'firma.html',
  'Format.dc.html': 'format.html',
  'Ponsel.dc.html': 'ponsel.html',
  'Batas.dc.html': 'batas.html',
  'Sambung.dc.html': 'sambung.html',
};
const tautan = (nama) => (nama === 'Main.dc.html' ? '/' : '/' + alamat[nama].replace(/\.html$/, ''));

const atributBoolean = ['checked', 'disabled', 'selected', 'hidden', 'readonly', 'required'];

function nilaiData(html) {
  const m = html.match(/<script type="text\/x-dc"[^>]*>([\s\S]*?)<\/script>/);
  if (!m) return {};
  const ctx = { DCLogic: class {} };
  vm.runInNewContext(`${m[1]}\n;globalThis.__nilai = new Component().renderVals();`, ctx);
  return ctx.__nilai || {};
}

function ambil(jalur, cakupan) {
  return jalur.split('.').reduce((o, k) => (o == null ? undefined : o[k]), cakupan);
}

function isiNilai(teks, cakupan) {
  // Atribut boolean yang bernilai false dihapus seluruhnya
  teks = teks.replace(new RegExp(`\\s(${atributBoolean.join('|')})="\\{\\{([^}]+)\\}\\}"`, 'g'), (_, attr, j) => {
    const v = ambil(j.trim(), cakupan);
    return v && v !== 'false' ? ` ${attr}` : '';
  });
  return teks.replace(/\{\{([^}]+)\}\}/g, (_, j) => {
    const v = ambil(j.trim(), cakupan);
    return v == null ? '' : String(v);
  });
}

function ulangi(html, cakupan) {
  const pola = /<sc-for list="\{\{([^}]+)\}\}" as="([^"]+)"[^>]*>([\s\S]*?)<\/sc-for>/;
  let m;
  while ((m = html.match(pola))) {
    const daftar = ambil(m[1].trim(), cakupan) || [];
    const isi = daftar.map((item) => isiNilai(m[3], { ...cakupan, [m[2]]: item })).join('');
    html = html.slice(0, m.index) + isi + html.slice(m.index + m[0].length);
  }
  return isiNilai(html, cakupan);
}

function rakit(nama) {
  let html = readFileSync(join(sumber, nama), 'utf8');
  const data = nilaiData(html);
  html = html
    .replace(/<script src="\.\/support\.js"><\/script>\n?/, '')
    .replace(/<script type="text\/x-dc"[\s\S]*?<\/script>\n?/, '')
    .replace('<meta charset="utf-8">', '<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">');
  // Isi <helmet> dipindah ke <head>, pembungkus <x-dc> dilepas
  const helmet = html.match(/<helmet>([\s\S]*?)<\/helmet>\n?/);
  if (helmet) {
    html = html.replace(helmet[0], '').replace('</head>', `${helmet[1]}</head>`);
  }
  html = html.replace(/<\/?x-dc>\n?/g, '');
  html = ulangi(html, data);
  html = html.replace(/href="([A-Za-z]+\.dc\.html)(#[^"]*)?"/g, (s, f, h = '') => (alamat[f] ? `href="${tautan(f)}${h}"` : s));
  return html;
}

rmSync(keluaran, { recursive: true, force: true });
mkdirSync(keluaran, { recursive: true });
for (const nama of readdirSync(sumber).filter((f) => f.endsWith('.dc.html'))) {
  if (!alamat[nama]) throw new Error(`Desain tanpa alamat: ${nama}`);
  writeFileSync(join(keluaran, alamat[nama]), rakit(nama));
  console.log(`${nama} -> ${alamat[nama]}`);
}
