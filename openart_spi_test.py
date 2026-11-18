from machime import SPI

spi = SPI(30)

spi.init(10000000, 0, 0, 0, SPI.MSB)

spi.write("hello")
spi.read(5)
