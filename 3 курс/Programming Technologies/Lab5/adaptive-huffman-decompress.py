import huffmancoding

def decompress(bitin, out):
	initfreqs = [1] * 257
	freqs = huffmancoding.FrequencyTable(initfreqs)
	dec = huffmancoding.HuffmanDecoder(bitin)
	dec.codetree = freqs.build_code_tree()
	count = 0
	while True:
		symbol = dec.read()
		if symbol == 256:
			break
		out.write(bytes((symbol,)))
		count += 1

		freqs.increment(symbol)
		if (count < 262144 and is_power_of_2(count)) or count % 262144 == 0:  # Update code tree
			dec.codetree = freqs.build_code_tree()
		if count % 262144 == 0:
			freqs = huffmancoding.FrequencyTable(initfreqs)

def is_power_of_2(x):
	return x > 0 and x & (x - 1) == 0

if __name__ == "__main__":
	inputfile = "compressData"
	outputfile = "decompressData.ppm"

	with open(inputfile, "rb") as inp, open(outputfile, "wb") as out:
		decompress(huffmancoding.BitInputStream(inp), out)
