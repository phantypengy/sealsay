class Sealsay < Formula
  desc "CLI app that generates ASCII art of a seal saying a message"
  homepage "https://github.com/phantypengy/sealsay"
  url "https://github.com/phantypengy/sealsay/archive/v1.1.1.tar.gz"
  sha256 "e8e37fc2e3076d883d8cde1aebc63aa5fe9eec284138a153af0245fc6e526a66"
  license "GPL-3.0-or-later"

  depends_on "python3"

  def install
    bin.install "sealsay"
    (share/"sealsay/seals").install Dir["seals/*"]
  end
end