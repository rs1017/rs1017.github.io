---
layout: post
title: "Flutter로 방치형 RPG 게임 만들기 - 김봉식 키우기 개발기"
date: 2026-02-10 18:00:00 +0900
categories: [Career]
tags: [flutter, flame-engine, game-dev, idle-rpg, mobile-game, dart]
description: "Flutter + Flame Engine으로 방치형 RPG 게임 '김봉식 키우기'를 개발하는 과정. 16년차 게임 서버 개발자가 클라이언트 개발에 도전한 이야기."
---

## 개요

16년차 게임 서버 개발자인 제가 처음으로 클라이언트 게임 개발에 도전했습니다.
**"김봉식 키우기"**라는 방치형(Idle) RPG 게임을 Flutter + Flame Engine으로 만들고 있습니다.

서버 개발자가 모바일 게임을 만들면 어떻게 될까요?
데이터 중심 설계, CSV 기반 기획 데이터 관리, 그리고 AI를 활용한 에셋 생성까지.
이 글에서는 개발 과정과 핵심 기술을 소개합니다.

## 김봉식 키우기란?

### 게임 컨셉

**"40대 중년 기사 김봉식이 월급쟁이 기사로 살아가는 이야기"**

- **장르**: 방치형(Idle) RPG + 클리커
- **플랫폼**: Windows, Web (추후 Android/iOS)
- **타겟**: 20~40대 직장인 (공감 가능한 스토리)

### 핵심 게임플레이

```
1. 몬스터 자동 사냥 → 골드 획득
2. 무기 업그레이드 → 전투력 상승
3. 층수 올리기 → 더 강한 몬스터
4. 퀘스트 달성 → 보상 획득
5. 환생 → 영구 스탯 증가
```

**방치형의 핵심**: 게임을 끄고 있어도 자동으로 사냥해서 골드를 모아줍니다.

## 왜 Flutter + Flame인가?

### 기술 스택 선택 배경

**1. Flutter (UI 프레임워크)**
- 크로스 플랫폼 (Windows, Web, Android, iOS 동시 지원)
- Hot Reload (빠른 개발 사이클)
- 서버 개발자도 배우기 쉬운 Dart 언어

**2. Flame Engine (게임 엔진)**
- Flutter 위에서 동작하는 2D 게임 엔진
- ECS 패턴 (Entity-Component-System)
- 물리 엔진, 애니메이션, 충돌 감지 내장

### Unity/Godot 대신 Flutter를 선택한 이유

| 항목 | Unity | Godot | **Flutter + Flame** |
|------|-------|-------|---------------------|
| 러닝 커브 | 높음 | 중간 | **낮음** |
| 크로스 플랫폼 | O | O | **O (웹 포함)** |
| Hot Reload | X | X | **O** |
| 빌드 속도 | 느림 | 빠름 | **매우 빠름** |
| 서버 개발자 친화성 | X | △ | **O** |

결론: **빠르게 프로토타입 만들고 검증**하기에 Flutter가 최적이었습니다.

## 프로젝트 구조

### 디렉토리 구조

```
lib/
├── main.dart                    # 앱 진입점
├── game/
│   ├── bongshik_game.dart      # Flame Game 메인 클래스
│   ├── game_state.dart         # 게임 상태 관리
│   ├── components/             # 게임 오브젝트
│   │   ├── player_component.dart      # 플레이어 (김봉식)
│   │   ├── monster_component.dart     # 몬스터
│   │   ├── effect_component.dart      # 타격 이펙트
│   │   └── background_component.dart  # 배경
│   ├── ui/                     # 게임 내 UI
│   │   ├── hud_overlay.dart           # 상단 HUD (골드, 층수)
│   │   ├── bottom_menu.dart           # 하단 메뉴
│   │   ├── weapon_panel.dart          # 무기 강화 패널
│   │   ├── quest_panel.dart           # 퀘스트 패널
│   │   ├── treasure_panel.dart        # 보물 패널
│   │   └── stat_panel.dart            # 스탯 패널
│   └── systems/                # 게임 시스템
│       ├── quest_system.dart          # 퀘스트 관리
│       ├── weapon_system.dart         # 무기 관리
│       └── rebirth_system.dart        # 환생 시스템
├── data/
│   ├── csv_loader.dart         # CSV 파싱
│   ├── game_data.dart          # 기획 데이터 모델
│   └── save_manager.dart       # 저장/로드
└── models/                     # 데이터 모델
    ├── player_model.dart
    ├── monster_model.dart
    ├── weapon_model.dart
    ├── quest_model.dart
    └── treasure_model.dart

assets/
├── data/                       # CSV 기획 데이터
│   ├── weapons.csv            # 무기 데이터
│   ├── quests.csv             # 퀘스트 데이터
│   ├── treasures.csv          # 보물 데이터
│   ├── monsters.csv           # 몬스터 데이터
│   ├── floors.csv             # 층수별 설정
│   └── costumes.csv           # 코스튬 데이터
└── images/                     # 게임 그래픽
    ├── characters/
    ├── monsters/
    ├── backgrounds/
    ├── ui/
    ├── weapons/
    └── effects/
```

## 핵심 기술

### 1. CSV 기반 기획 데이터 관리

**서버 개발자의 습관**: 모든 기획 데이터는 CSV로 관리합니다.

`assets/data/weapons.csv`
```csv
id,name,baseAttack,costMultiplier,description
1,녹슨 검,10,1.15,회사에서 지급한 낡은 검
2,철검,50,1.15,월급으로 산 철제 검
3,강철검,250,1.15,보너스로 장만한 강철 검
4,마법검,1250,1.15,퇴직금으로 산 마법 검
```

`lib/data/csv_loader.dart`
```dart
class CsvLoader {
  static Future<List<Weapon>> loadWeapons() async {
    final data = await rootBundle.loadString('assets/data/weapons.csv');
    final rows = const CsvToListConverter().convert(data);

    return rows.skip(1).map((row) => Weapon(
      id: row[0],
      name: row[1],
      baseAttack: row[2],
      costMultiplier: row[3],
      description: row[4],
    )).toList();
  }
}
```

**장점**:
- ✅ 코드 수정 없이 밸런스 조정 가능
- ✅ 기획자가 직접 Excel에서 수정 가능
- ✅ Git으로 데이터 변경 이력 추적
- ✅ 서버 개발 경험 그대로 활용

### 2. Flame Engine 컴포넌트 시스템

**ECS 패턴**: 플레이어, 몬스터, 이펙트 모두 Component입니다.

`lib/game/components/player_component.dart`
```dart
class PlayerComponent extends SpriteAnimationComponent {
  final GameState gameState;

  PlayerComponent({required this.gameState})
      : super(size: Vector2(64, 64), anchor: Anchor.center);

  @override
  Future<void> onLoad() async {
    // 스프라이트 애니메이션 로드
    animation = await game.loadSpriteAnimation(
      'characters/bongshik.png',
      SpriteAnimationData.sequenced(
        amount: 4,
        stepTime: 0.2,
        textureSize: Vector2(64, 64),
      ),
    );

    position = Vector2(100, game.size.y / 2);
  }

  @override
  void update(double dt) {
    super.update(dt);

    // 자동 공격 (1초마다)
    if (gameState.canAttack()) {
      _attack();
      gameState.resetAttackCooldown();
    }
  }

  void _attack() {
    // 타격 이펙트 생성
    game.add(EffectComponent(position: position));

    // 몬스터에게 데미지
    gameState.dealDamage();
  }
}
```

**Flame의 라이프사이클**:
1. `onLoad()`: 초기화 (스프라이트 로드)
2. `update(dt)`: 매 프레임 실행 (게임 로직)
3. `render(canvas)`: 화면 그리기 (선택)

### 3. 상태 관리 (Provider 패턴)

`lib/game/game_state.dart`
```dart
class GameState extends ChangeNotifier {
  // 플레이어 스탯
  BigInt gold = BigInt.from(0);
  BigInt damage = BigInt.from(10);
  int floor = 1;

  // 몬스터 상태
  BigInt monsterHp = BigInt.from(100);
  BigInt monsterMaxHp = BigInt.from(100);

  // 무기 시스템
  List<Weapon> weapons = [];
  Map<int, int> weaponLevels = {};

  // 공격 처리
  void dealDamage() {
    monsterHp -= damage;

    if (monsterHp <= BigInt.zero) {
      _killMonster();
    }

    notifyListeners(); // UI 업데이트
  }

  void _killMonster() {
    // 골드 획득
    gold += _calculateGoldReward();

    // 다음 몬스터 스폰
    _spawnNextMonster();

    notifyListeners();
  }

  // 무기 업그레이드
  void upgradeWeapon(int weaponId) {
    final cost = _calculateUpgradeCost(weaponId);

    if (gold >= cost) {
      gold -= cost;
      weaponLevels[weaponId] = (weaponLevels[weaponId] ?? 0) + 1;

      // 데미지 재계산
      damage = _recalculateDamage();

      notifyListeners();
    }
  }
}
```

**Provider 패턴의 장점**:
- UI가 자동으로 반응 (`notifyListeners()` 호출 시)
- 전역 상태 관리 (어디서든 접근 가능)
- 테스트 용이

### 4. 저장/로드 시스템

`lib/data/save_manager.dart`
```dart
class SaveManager {
  static const String _keyGameState = 'game_state';

  static Future<void> save(GameState state) async {
    final prefs = await SharedPreferences.getInstance();

    // GameState를 JSON으로 직렬화
    final data = {
      'gold': state.gold.toString(),
      'damage': state.damage.toString(),
      'floor': state.floor,
      'weaponLevels': state.weaponLevels,
      'lastSaveTime': DateTime.now().toIso8601String(),
    };

    await prefs.setString(_keyGameState, jsonEncode(data));
  }

  static Future<GameState?> load() async {
    final prefs = await SharedPreferences.getInstance();
    final jsonString = prefs.getString(_keyGameState);

    if (jsonString == null) return null;

    final data = jsonDecode(jsonString);

    // 방치 보상 계산
    final lastSaveTime = DateTime.parse(data['lastSaveTime']);
    final offlineTime = DateTime.now().difference(lastSaveTime);
    final offlineGold = _calculateOfflineGold(offlineTime);

    // GameState 복원
    return GameState.fromJson(data, offlineGold: offlineGold);
  }

  static BigInt _calculateOfflineGold(Duration offlineTime) {
    // 최대 4시간까지만 보상
    final hours = min(offlineTime.inHours, 4);
    // 시간당 초당 골드 * 3600초
    return BigInt.from(hours * 3600 * 100);
  }
}
```

**방치형 게임의 핵심**: 오프라인 보상!

### 5. 큰 숫자 처리 (BigInt)

방치형 게임은 숫자가 기하급수적으로 커집니다.

```dart
// ❌ int로는 부족 (최대 2^63-1)
int gold = 999999999999999999; // 오버플로우 위험

// ✅ BigInt 사용
BigInt gold = BigInt.parse('999999999999999999999999');

// 연산
gold += BigInt.from(1000);
gold *= BigInt.from(2);

// 표시 (K, M, B, T 단위)
String formatBigInt(BigInt value) {
  if (value < BigInt.from(1000)) return value.toString();
  if (value < BigInt.from(1000000)) {
    return '${(value / BigInt.from(1000)).toStringAsFixed(1)}K';
  }
  if (value < BigInt.from(1000000000)) {
    return '${(value / BigInt.from(1000000)).toStringAsFixed(1)}M';
  }
  return '${(value / BigInt.from(1000000000)).toStringAsFixed(1)}B';
}
```

## AI를 활용한 게임 에셋 생성

### Stable Diffusion WebUI로 캐릭터 생성

**프롬프트 예시**:
```
Positive Prompt:
"pixel art, 8-bit style, middle-aged knight character,
tired office worker, simple design, side view,
animation sprite sheet, 4 frames walking cycle"

Negative Prompt:
"realistic, 3d, detailed, complex, modern, colorful"

Settings:
- Model: Pixel Art XL
- Size: 256x64 (4 frames)
- Steps: 30
- CFG Scale: 7
```

> 📌 **실제 생성 이미지**: Claude.ai WebUI Artifacts로 픽셀 아트 스프라이트 생성 가능

### 배경 생성

```
Positive Prompt:
"pixel art background, dark cave dungeon,
simple parallax layers, 8-bit game,
repeatable tileable pattern"
```

## 현재 진행 상황

### 완성된 기능 ✅

- [x] 기본 게임 루프 (플레이어, 몬스터, 자동 전투)
- [x] 무기 시스템 (업그레이드, 레벨업)
- [x] 퀘스트 시스템 (일일 퀘스트, 도전 과제)
- [x] 저장/로드 (SharedPreferences)
- [x] 방치 보상 (오프라인 골드)
- [x] CSV 기획 데이터 관리
- [x] HUD UI (골드, 층수, DPS)
- [x] 하단 메뉴 (무기, 퀘스트, 보물, 스탯)

### 개발 중인 기능 🚧

- [ ] 환생 시스템 (영구 스탯)
- [ ] 보물 시스템 (패시브 효과)
- [ ] 스킬 시스템 (액티브 스킬)
- [ ] 보스 전투
- [ ] 코스튬 시스템
- [ ] 업적 시스템

### 계획 중인 기능 📋

- [ ] 멀티플레이 (랭킹, 길드)
- [ ] 이벤트 (기간 한정 던전)
- [ ] 결제 시스템 (광고 제거, 프리미엄 패스)

## 개발하면서 배운 것

### 1. Flutter는 생각보다 강력하다

**서버 개발자의 시각에서**:
- Hot Reload = 빠른 개발 사이클 (서버의 nodemon 같은 느낌)
- Widget 트리 = React의 Component 트리
- Provider = Redux/Context API
- 크로스 플랫폼 = "Write Once, Run Anywhere" (진짜 됨!)

### 2. 게임 개발은 데이터 설계가 핵심

**서버 개발 경험이 도움됨**:
- CSV 기반 데이터 관리 → 게임 밸런스 조정 용이
- 상태 관리 패턴 → 버그 적은 코드
- 저장/로드 로직 → DB 설계 경험 활용

### 3. AI로 에셋 생성은 현실이다

**Stable Diffusion WebUI**:
- 캐릭터 스프라이트 (5분)
- 배경 (10분)
- UI 아이콘 (3분)

**전통 방식 대비 시간 절약**: 80~90%

## 실행 방법

### 환경 설정

```bash
# 1. Flutter 설치
# https://docs.flutter.dev/get-started/install

# 2. 프로젝트 클론
git clone https://github.com/your-repo/bongshik_growing.git
cd bongshik_growing

# 3. 의존성 설치
flutter pub get

# 4. 실행
flutter run -d windows  # Windows
flutter run -d chrome   # Web
```

### 시스템 요구사항

- **Windows**: Windows 10 이상
- **Flutter**: 3.0 이상
- **Dart**: 3.0 이상

## 다음 단계

### 단기 목표 (1개월)
1. 환생 시스템 완성
2. 보스 전투 추가
3. Android 빌드 및 테스트

### 중기 목표 (3개월)
1. Google Play 출시
2. 광고 수익화
3. 유저 피드백 반영

### 장기 목표 (6개월)
1. 멀티플레이 기능
2. 이벤트 시스템
3. 월 매출 100만원 달성

## 마무리

16년간 서버만 개발하다가 처음으로 클라이언트 게임을 만들어봤습니다.

**배운 점**:
- Flutter는 서버 개발자도 쉽게 배울 수 있다
- 게임 개발도 결국 데이터 설계가 핵심이다
- AI 도구로 혼자서도 게임을 만들 수 있다

**다음 글 예고**:
- [Flutter Flame Engine 완벽 가이드 - ECS 패턴으로 게임 만들기](/posts/flutter-flame-ecs-guide)
- [Stable Diffusion으로 게임 에셋 생성하기 - 픽셀 아트 편](/posts/stable-diffusion-pixel-art)

---

**프로젝트 저장소**: [GitHub - Kim Bongshik Growing Game](https://github.com/...)
**플레이 테스트**: 곧 공개 예정

**질문/피드백**:
댓글로 자유롭게 남겨주세요!

---

**함께 읽으면 좋은 글**:
- [게임 서버 개발자의 커리어 전환 이야기](/posts/career-transition)
- [Flutter로 크로스 플랫폼 앱 개발하기](/posts/flutter-cross-platform)
