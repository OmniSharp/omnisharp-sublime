# 개요
Sublime Text 3용 C# IDE 플러그인입니다. OmniSharpServer를 사용했으며, 비동기 통신으로
에디터가 느려지는 것은 최소화하였습니다.

현재 Mac OSX만 지원합니다.

# 필요 사항
1. mono

# 설치 방법
1. 터미널로 sublime 플러그인 디렉토리로 이동합니다.

    cd /Users/master/Library/Application\ Support/Sublime\ Text\ 3/Packages

2. git으로 OmniSharpSublime을 받습니다.

    git clone https://github.com/moonrabbit/OmniSharpSublime.git
    git submodule update --init

3. OmniSharpSublime 디펙토리로 이동한 뒤, build.sh 스크립트를 실행해 줍니다.

    cd OmniSharpSublime
    ./build.sh

# 사용법
sublime text project 파일에 솔루션 위치만 지정해주면 사용이 가능합니다.

##설정 파일의 예

        {
            "folders":
            [
                {
                    "name": "fxd_client",
                    "follow_symlinks": true,
                    "path": ".",
                    "file_exclude_patterns":
                    [
                        "*.meta",
                        "*.png",
                        "*.dll",
                        "*.mdb"
                    ],
                    "folder_exclude_patterns":
                    [
                        "Library"
                    ]
                }
            ],
            "settings":
            {
                "tab_size": 4
            },
            "solution_file": "./fxd_client-csharp.sln"
        }


# 참고

3가지 프로젝트를 참고하고 있습니다.

1. anaconda (sublime text용 python IDE 플러그인) :
https://github.com/DamnWidget/anaconda
2. Omnisharp (vim용 C# IDE 플러그인) :
https://github.com/nosami/Omnisharp
3. OmniSharpSublime by n-yoda :
https://github.com/n-yoda/OmniSharpSublime

# TODO
* Find Usage
* Syntax error
* Show Documentations
* Find type / symbols
* code action
* code format
* type lookup
* syntax highlight 강화(vim용 Omnisharp 참고)
