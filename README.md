# RGB Splitter (RGGB CFA to RGB)

**English** | [Türkçe](#türkçe)

## English

### Overview
**RGB Splitter** is a command-line interface (CLI) tool designed to split scientific FITS images containing an RGGB Color Filter Array (CFA) pattern into separate Red, Green, and Blue FITS files.

Unlike traditional de-mosaicing algorithms that interpolate pixel values to maintain resolution, this tool uses a **Superpixel Extraction** method. It treats each 2x2 Bayer block as a single superpixel source, extracting:
- **Red:** Top-left pixel
- **Green:** Average of top-right and bottom-left pixels
- **Blue:** Bottom-right pixel

This process reduces the image resolution by half (width/2, height/2) but preserves the raw radiometric data of the pixels without introducing interpolation artifacts. It also automatically updates the FITS header WCS (World Coordinate System) keywords defined in the header to match the new geometry.

### Installation
Prerequisites: Python 3.10+

### Dependencies
- numpy>=1.23
- astropy>=5.3
- tqdm>=4.66

You can install the package directly from GitHub or from source.

#### Option 1: Install from GitHub (Recommended)
You can install the latest version directly using pip:

```bash
pip install git+https://github.com/ycanatilgan/rgb_splitter.git
```

#### Option 2: Install from Source
1. Clone or download this repository.
   ```bash
   git clone https://github.com/ycanatilgan/rgb_splitter.git
   ```
2. Navigate to the project directory.
   ```bash
   cd rgb_splitter
   ```
3. Install using pip:
   ```bash
   pip install .
   ```

### Usage

Run the tool from your terminal using the `rgb-split` command.

#### Basic Usage
Process all FITS files in the `./data` directory (recursive). The output will be saved in `./data/rgb_split` by default.

```bash
rgb-split --input ./data
```

#### Custom Output Directory
Specify a custom destination for the processed files.

```bash
rgb-split --input ./raw_images --output ./processed_images
```

#### Parallel Processing
Speed up processing by specifying the number of worker processes (threads). By default, it uses `CPU Count - 1`.

```bash
rgb-split -i ./data -w 8
```

#### Resume Capability
The tool automatically checks if the output files (R, G, and B) already exist. If they do, it skips the file, allowing you to resume interrupted jobs easily.

### Output Structure
The tool maintains the directory structure of the input folder relative to the output folder. Inside each leaf directory, it creates `R`, `G`, and `B` subdirectories.

```
output_dir/
└── subfolder/
    ├── R/
    │   └── image.fits
    ├── G/
    │   └── image.fits
    └── B/
        └── image.fits
```

---

## Türkçe

### Genel Bakış
**RGB Splitter**, RGGB Bayer filtresine (CFA) sahip FITS formatındaki astronomi/bilimsel görüntülerini, ayrı Kırmızı (R), Yeşil (G) ve Mavi (B) kanallarına ayıran bir komut satırı aracıdır.

Pikselleri enterpole ederek (uydurarak) çözünürlüğü korumaya çalışan geleneksel yöntemlerin aksine, bu araç **Süper-piksel Çıkarımı (Superpixel Extraction)** yöntemini kullanır. Her 2x2'lik Bayer bloğunu tek bir kaynak olarak ele alır:
- **Kırmızı:** Sol üst piksel
- **Yeşil:** Sağ üst ve sol alt piksellerin ortalaması
- **Mavi:** Sağ alt piksel

Bu işlem görüntü çözünürlüğünü yarıya düşürür (genişlik/2, yükseklik/2), ancak interpolasyon hataları (artifact) oluşturmadan ham piksel verisini korur. Ayrıca FITS başlığındaki WCS (Dünya Koordinat Sistemi) verilerini yeni geometriye uygun olarak otomatik günceller.

### Kurulum
Gereksinimler: Python 3.10+

### Bağımlılıklar (Dependencies)
- numpy>=1.23
- astropy>=5.3
- tqdm>=4.66

Paketi doğrudan GitHub üzerinden veya kaynak koddan kurabilirsiniz.

#### Seçenek 1: GitHub Üzerinden Kurulum (Önerilen)
En güncel sürümü pip kullanarak doğrudan kurabilirsiniz:

```bash
pip install git+https://github.com/ycanatilgan/rgb_splitter.git
```

#### Seçenek 2: Kaynak Koddan Kurulum
1. Projeyi klonlayın veya indirin.
   ```bash
   git clone https://github.com/ycanatilgan/rgb_splitter.git
   ```
2. Proje dizinine gidin.
   ```bash
   cd rgb_splitter
   ```
3. pip ile kurulumu yapın:
   ```bash
   pip install .
   ```

### Kullanım

Terminalinizden `rgb-split` komutunu kullanarak aracı çalıştırabilirsiniz.

#### Temel Kullanım
`./data` klasöründeki tüm FITS dosyalarını (alt klasörler dahil) işler. Çıktılar varsayılan olarak `./data/rgb_split` klasörüne kaydedilir.

```bash
rgb-split --input ./data
```

#### Özel Çıktı Klasörü Belirleme
İşlenen dosyaların kaydedileceği yeri kendiniz belirleyebilirsiniz.

```bash
rgb-split --input ./ham_goruntuler --output ./islenmis_goruntuler
```

#### Paralel İşleme (Hızlandırma)
İşlemci çekirdeklerini kullanarak dönüştürme işlemini hızlandırabilirsiniz. Varsayılan olarak `Toplam Çekirdek - 1` kadar işlemci kullanılır.

```bash
rgb-split -i ./data -w 8
```

#### Kaldığı Yerden Devam Etme (Resume)
Araç, çıktı dosyalarının (R, G ve B) hedef klasörde var olup olmadığını kontrol eder. Eğer dosyalar mevcutsa işlem atlanır. Bu sayede yarıda kalan işlemleri kolayca devam ettirebilirsiniz.

### Çıktı Yapısı
Araç, giriş klasöründeki dosya ve klasör hiyerarşisini çıktı klasöründe de korur. Her klasörün içinde `R`, `G` ve `B` alt klasörleri oluşturulur.

```
cikti_klasoru/
└── alt_klasor/
    ├── R/
    │   └── goruntu.fits
    ├── G/
    │   └── goruntu.fits
    └── B/
        └── goruntu.fits
```
