# SPEC.md — AI Expense Categorizer

## 1. Tujuan
Sistem otomatis mengelompokkan tiap pengeluaran ke kategori yang tepat, supaya tidak perlu pilih kategori manual tiap input, dan bisa melihat pola pengeluaran per kategori.

## 2. Input
- `description` (string, teks bebas, tidak terstruktur)
- `amount` (format bebas — bisa "150rb", "170.000", atau "20000")

Contoh nyata:
- description: "pulsa", amount: "150rb"
- description: "cuci muka", amount: "207000"
- description: "whey protein", amount: "1700000"
- description: "topup game", amount: "170.000"
- description: "snack", amount: "20000"

Catatan: sistem menerima format amount bebas — akan dinormalisasi/parsing menjadi angka murni sebelum diproses (lihat Edge Case).

## 3. Output
```json
{
  "category": "food",
  "confidence": "high"
}
```
`confidence` bernilai "low" ketika ada dua atau lebih opsi kategori yang sama-sama masuk akal untuk input tersebut.

## 4. Constraint
- Kategori valid HANYA: `Food`, `Hiburan`, `Self Reward`, `Self Development`, `Lainnya`
- AI tidak boleh membuat kategori baru di luar daftar ini, kecuali user (Ismail) yang secara eksplisit meminta penambahan kategori
- Jika AI mengembalikan kategori di luar daftar → sistem otomatis masukkan ke `"Lainnya"`

## 5. Edge Case
| Skenario | Penanganan |
|---|---|
| `description` benar-benar kosong (tidak ada input) | Tolak, minta user isi ulang |
| `description` ada tapi tidak informatif (mis. cuma "bayar 50000" tanpa konteks) | Terima, kategorikan sebagai `"Lainnya"`, `confidence: "low"` |
| `amount` berformat bebas (mis. "20rb", "20.000") | Sistem normalisasi/parsing jadi angka murni |
| Server/API AI down atau error saat dipanggil | Expense tetap disimpan, tanpa kategori, ditandai untuk diproses ulang nanti |
| AI kembalikan kategori di luar daftar Constraint | Otomatis dialihkan ke `"Lainnya"` |
