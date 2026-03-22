class Sealsay < Formula
  desc "CLI app that generates ASCII art of a seal saying a message"
  homepage "https://github.com/phantypengy/sealsay"
  url "https://github.com/phantypengy/sealsay/archive/v1.1.1.tar.gz"
  sha256 "eae7f28e4afd412f6e9c62f5cb98d7c797283348ce763229ee600505c6d72cf7"
  license "GPL-3.0-or-later"

  depends_on "python3"

  def install
    bin.install "sealsay"
    (share/"sealsay/seals").install Dir["seals/*"]
  end
end