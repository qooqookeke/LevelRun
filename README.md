# LevelRun
[프로젝트 기획]

새해에는 많은 사람들이 건강 증진을 위해 헬스장이나 피트니스 센터를 찾으며 건강한 생활을 추구합니다. 그러나 이러한 목표는 종종 짧은 시간 안에 끝나버리는 경향이 있습니다. 따라서 이러한 문제를 해결하고 운동 습관을 장기적으로 유지할 수 있도록 하는 앱을 개발하였습니다.

1. 위치 기반 캐릭터 획득\n
Google Map API 및 Google Places API를 활용하여 사용자의 위치와 주변에 있는 캐릭터를 얻을 수 있는 랜덤 상자를 제공합니다. 이를 통해 사용자들은 운동을 하면서 재미를 더하고 동기부여를 받을 수 있습니다.

2. 텍스트 음성 변환
사용자가 운동 중에 핸드폰을 자주 사용하지 않도록 Google Text-to-Speech API를 활용하여 텍스트를 음성으로 변환하여 제공합니다. 이를 통해 운동 도중에도 사용자는 휴대폰을 사용하지 않고도 필요한 정보를 얻을 수 있습니다.

3. 날씨 정보 확인
 OpenWeather API를 통해 사용자들은 운동을 하기 전에 현재 날씨 정보와 3시간별 날씨 정보, 대기 오염 지수를 확인할 수 있습니다.

4. 레벨 시스템 및 랭킹
사용자들 간에 경쟁을 유도하기 위해 레벨 시스템과 랭킹 시스템을 도입하였습니다. 사용자들은 운동을 통해 경험치를 획득하고 랭킹을 올려 자신의 운동능력을 측정할 수 있습니다.

5. 캐릭터 수집
포켓몬 GO를 벤치마킹하여 운동 중에 얻은 랜덤 상자를 통해 다양한 종류의 캐릭터를 얻을 수 있습니다. 또한 수집한 캐릭터 목록을 통해 사용자는 자신이 어떤 캐릭터를 모았는지 확인할 수 있습니다.

6. 자동 태깅 시스템
인스타그램을 벤치마킹하여 소셜 기능을 추가하였습니다. 사용자는 이미지를 업로드하고 다른 사용자들과 공유할 수 있으며, 이미지를 업로드할 때 AWS의 Rekognition API를 활용하여 이미지에 대한 자동 태깅 시스템을 구현하였습니다.