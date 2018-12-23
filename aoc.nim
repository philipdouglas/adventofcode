import httpclient
import os
import rdstdin
import strformat
import strutils


proc getSession(): string =
    let sessionFileName = ".aoc_session"
    if sessionFileName.existsFile:
        result = sessionFileName.readFile.strip()
    else:
        echo "Error! Put your AOC session id in .aoc_session"


let
    cacheDir = ".cache"
    sessionId = getSession()


proc input*(day: int, year: int = 2018): string =
    if not cacheDir.existsDir:
        cacheDir.createDir

    let cacheFileName = cacheDir.joinPath(&"input_{year}_{day:02}.txt")

    if cacheFileName.existsFile:
        result = cacheFileName.readFile
    else:
        var client = newHttpClient()
        client.headers = newHttpHeaders({
            "Cookie": &"session={sessionId}"
        })
        result = client.getContent(&"https://adventofcode.com/{year}/day/{day}/input")
        cacheFileName.writeFile(result)

    return result.strip(leading=false, trailing=true, chars={'\n'})


proc pause*(prompt: string = ".") =
    discard readLineFromStdin(prompt)


when isMainModule:
    pause(input(day=1, year=2016))
