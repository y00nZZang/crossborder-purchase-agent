# Crossborder Purchase — experimental 0.1.0

상품 탐색·배송대행 견적·승인된 라쿠텐 북스 구매·몰테일 신청·배송 추적을 연결하는 Codex skills 패키지입니다. Python 3.10+ 표준 라이브러리만 사용하며 별도 API 키가 필요하지 않습니다. 브라우저·Gmail·예약 작업은 실행하는 Codex 환경의 연결 도구를 이용합니다.

## 구성과 현재 지원

| 구성 | 구현 |
| --- | --- |
| `crossborder-prepare-purchase` | 상품/판매처 제한 없는 탐색 지침, JSON-LD 후보 추출 helper |
| `crossborder-compare-forwarders` | 3개 업체 조사 절차, JPY/KRW 계산, 동등 조건·누락·만료 검증 |
| `crossborder-purchase-rakuten` | 구매 흐름 skill, 승인 결합·조건 대조·시도 기록 helper |
| `crossborder-register-malltail` | 현재 관측한 폼 지도, 기존 신청 대조·운송장 보완 절차 |
| `crossborder-track-delivery` | 메일/사이트 대조·반복 작업 지침, 이벤트/조회 결과 기록 helper |

**skills가 브라우저를 조작하고 Python 도구가 계산·상태를 관리합니다.** 고정 셀렉터만으로 실행되는 무인 구매 봇이나 상시 서버는 아닙니다. 2026-10-05 별도 세션에서 설치된 플러그인으로 주문 결과 확인과 몰테일 접수를 검증했습니다. 최종 구매 버튼과 로그인·추가 인증은 사용자가 수행했습니다. 배송 완료는 미검증입니다. 몰테일 3·4단계와 소분류는 현재 화면 확인이 필요합니다. 관세 자동분류 엔진은 없으며 공식 자료 조사 결과를 견적에 반영합니다. 상태 기록은 에이전트가 입력한 근거의 진위를 독립 검증하지 않습니다.

## 시작하기

설치 전에는 Codex에 `plugin/skills/crossborder-prepare-purchase/SKILL.md`를 읽고 상품 URL을 조사하도록 요청할 수 있습니다. 설치된 경우 `$crossborder-prepare-purchase`를 호출합니다. 실제 구매 전 승인 단계가 있으며 조사 요청만으로 구매하지 않습니다.

예시 요청:

> 이 상품 URL을 조사하고 몰테일·tenso·転送JAPAN 견적을 비교해줘. 이번에는 dry-run으로 진행하고 구매나 신청서는 제출하지 마.

> 이 실행의 기존 주문과 몰테일 신청을 확인하고 현재 배송 상태를 알려줘. 새로운 주문은 하지 마.

로컬 helper:
```sh
python3 plugin/scripts/purchase_agent.py --help
python3 plugin/scripts/purchase_agent.py extract tests/fixtures/product.html --url https://example.com/product
python3 -m unittest discover -s tests -v
python3 scripts/package_plugin.py
```
입력 JSON과 명령별 계약은 [runtime.md](references/runtime.md)에 있습니다. 기본 상태는 `~/.local/share/crossborder-purchase/ledger.sqlite3`, 별도 위치는 `--state-dir` 또는 `PURCHASE_AGENT_STATE_DIR`로 지정합니다. 테스트는 임시 디렉터리만 사용합니다. JSON 초안·주문 식별자·DB는 공개 저장소나 배포 ZIP에 포함하지 않습니다.

## 패키징·설치 경계

`plugin.json`은 portable manifest, `.codex-plugin/plugin.json`은 Codex 호환 manifest입니다. 빌드 명령은 `dist/crossborder-purchase-0.1.0.zip`을 생성합니다. ZIP에는 skills, references, scripts와 manifest가 포함됩니다. 로컬 설치 후 별도 세션 실험을 진행했습니다. 공개 마켓플레이스 등록은 하지 않았습니다. 배포 형식은 [공식 패키징 안내](https://developers.openai.com/plugins/build/plugins)를 2026-10-05 확인했습니다.

선행 연결: 브라우저, Gmail 읽기, 추적을 예약할 경우 Codex 예약 작업 도구. 자동 연결·비밀번호 보관·쿠키 복제는 제공하지 않습니다. 로그인/추가 인증은 사용자가 준비합니다. 설치 여부와 도구 연결 여부를 구분합니다.

## 다음 실거래 검증

1. 취소된 원주문·환불·기존 몰테일 신청을 각각 대조.
2. 새 상품 URL로 최신 견적과 읽기 전용 dry-run.
3. 최종 조건 승인 후 주문 접수, 이어 배송신청 저장 내역 확인.
4. 단회 추적 성공 후 지정한 시간으로 반복 작업 등록.
5. 운송장 보완·실측 운임·수령과 실제 총비용 기록.
