[3, 4, 1, 5]
|> KnotHash.singleround(5)
|> IO.puts()

[76,1,88,148,166,217,130,0,128,254,16,2,130,71,255,229]
|> KnotHash.singleround()
|> IO.puts()

'1,2,3'
|> KnotHash.hex()
|> IO.puts()

'76,1,88,148,166,217,130,0,128,254,16,2,130,71,255,229'
|> KnotHash.hex()
|> IO.puts()
