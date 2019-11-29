import qualified Data.IntSet as Set

parseInput :: String -> [Int]
parseInput = map (read . filter (/= '+')) . lines

part1 :: [Int] -> Int
part1 = sum

part2 :: [Int] -> Int
part2 = check Set.empty . scanl (+) 0 . cycle
    where check set (freq:next)
            | freq `Set.member` set = freq
            | otherwise             = check (Set.insert freq set) next

main = do
    input <- readFile ".cache/input_2018_01.txt"
    let ints = parseInput input
    print (part1 ints)
    print (part2 ints)
