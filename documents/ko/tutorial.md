Unity + OmniSharpSublime
========================
OmniSharpSublime 은 **C#** 코드 관리를 위해 만들어진 **OS X** 용 **mono** 기반 Sublime Text **3** 플러그인입니다.

환경 준비
---------
Unity + OmniSharpSublime 를 사용하기 위해서는 다음과 같은 환경이 준비되어야 합니다.

* OS X <https://www.apple.com/kr/osx/>
* 서브라임3 <http://www.sublimetext.com/3>
* 유니티3D  <http://unity3d.com/unity/download>
* 모노 MRE(Mono Runtime Environement) <http://www.mono-project.com/download/>


플러그인 설치
-------------
Sublime 을 실행 한 후 메인 메뉴를 열어 `Sublime Text > Preferences > Browse Packages...`를 클릭합니다.

Packages 디렉토리에 OmniSharpSublime 플러그인<https://github.com/moonrabbit/OmniSharpSublime>을 다운로드 받아 압축을 해제하거나 직접 git clone 을 실행합니다.

    $ cd ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/

    $ git clone https://github.com/moonrabbit/OmniSharpSublime.git OmniSharpSublime

    $ cd OmniSharpSublime

    $ git submodule update --init --recursive

    $ ./build.sh

  
유니티 프로젝트 준비
--------------------
유니티를 실행해 새로운 프로젝트를 생성합니다. 이미 프로젝트를 가지고 있다면 건너뛰셔도 됩니다. 여기서는 프로젝트 이름을 OmniSharpSublime 로 사용하겠습니다.

    $ cd ~/Projects/OmniSharpSublime 

메인 메뉴 `Unity > Preferences` 를 클릭해 다이얼로그에서 External Tools 를 선택하고 External Script Editor 에서 Browse 를 선택해 응용 프로그램안에 들어 있는 Sublime Text 를 Open 합니다.

메인 메뉴 `Assets > Sync MonoDevelop Project`를 클릭해 모노 솔류션 파일을 생성합니다. 

Project Dock의 Assets 에 HelloWorld C# 스크립트를 생성한 다음, Hierachy Dock에 있는 게임 오브젝트에 연결 합니다.

Project Dock의 HelloWorld 를 클릭하면 Sublime Text 가 실행되면서 HelloWorld.cs 가 오픈됩니다.


서브라임 프로젝트 준비
----------------------
서브라임 메인 메뉴 `Project > Save Project As...`를 클릭해 서브라임 프로젝트를 생성합니다. 여기서는 OmniSharpSublime.sublime-project 라고 정하겠습니다. 저장 위치를 정하기 위해 파일 옆 아래 화살표를 눌러 Assets 가 아닌 프로젝트 루트 디렉토리(~/Projects/OmniSharpSublime)에 저장합니다.

메인 메뉴 `Project > Edit Project`를 오픈해 프로젝트 설정을 진행합니다.

    {
        "solution_file": "./OmniSharpSublime.sln",
        "folders":
        [
            {
                "name": "OmniSharpSublime",
                "path": ".",
                "file_exclude_patterns":
                [
                    "*.meta"
                ]
            }
        ],
        "settings":
        {
            "auto_complete_triggers": [
                {
                    "characters": ".", 
                    "selector": "source.cs"
                }
            ]
        }
    }

FAQ
---

#### 문제 확인 방법

서브라임 메인 메뉴 `View > Show Console`을 통해 로그를 확인 할 수 있습니다.


