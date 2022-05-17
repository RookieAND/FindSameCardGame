# FindSameCardGame

2022년도 3학년 1학기 데이터베이스 텀프로젝트.

## Description [프로젝트 소개]

javascript, html, scss 를 활용한 웹앱 기반 같은 카드 찾기 게임 사이트입니다.
현재 flask 프레임워크로 백엔드 파트를 구축 중이며, 추후 heroku에 서비스 될 예정입니다.


## Dependencies

* javascript
* HTML5
* CSS3, SCSS

## Game System [시스템 안내]

* 총 36장의 카드가 필드 위에 무작위하게 섞이며, 카드의 종류는 3~6종류입니다.
* 게임 시작 전 플레이어는 필드 위에 놓인 카드를 3초 간 열람할 수 있습니다.
* 이후 3초의 시간이 지나면, 필드 위에 놓인 카드가 자동으로 뒤집어집니다.
* 플레이어는 필드 위에 놓인 카드 중 짝이 같은 두 카드를 선택해야 합니다.
* 제한 시간은 60초이며, 36개의 카드를 모두 맞출 시 다음 스테이지로 넘어갑니다.
* 제한 시간이 모두 소거되었다면 게임이 종료되며, 자신의 최종 스코어가 출력됩니다.

## Authors [제작자]

* RookieAND_ (https://github.com/RookieAND)

## Version History

* 0.3
    * Add flask back-end part of minigame Web.
    * Add email-verification register system.
    * Add user profile, leaderboard, and statistic.
* 0.2
    * Add auto - stage difficulty setting system.
    * Add stage system and combo system.
    * change maximum limit time from 120 to 60.
* 0.1
    * Initial Release

## License

해당 프로젝트의 라이센스는 [MIT] License 규정을 지키고 있습니다.
