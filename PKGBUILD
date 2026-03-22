# Maintainer: Dominik Chwirot dchwirot01@gmail.com
pkgname=sealsay
pkgver=1.1.0
pkgrel=1
pkgdesc="CLI app that generates ASCII art of a seal saying a message"
arch=(any)
url="https://github.com/phantypengy/sealsay"
license=('GPL-3.0-or-later')
depends=(python)

source=("$pkgname-$pkgver.tar.gz::https://github.com/phantypengy/sealsay/archive/v$pkgver.tar.gz")
sha256sums=('65792fc66c5e679b80e1b796f2d5e3751f905b25358d4845b4dcf811492609e2')

package() {
    install -Dm755 "$srcdir/sealsay-$pkgver/sealsay" "$pkgdir/usr/bin/sealsay"
    install -Dm644 "$srcdir/sealsay-$pkgver/seals/"* "$pkgdir/usr/share/sealsay/seals/"
}