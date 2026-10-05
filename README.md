# Crossborder Purchase Agent

일본 상품의 조사·배송대행 비교·구매 준비·배송신청을 돕는 **Codex plugin 실험 프로젝트**입니다. Python helper는 계산과 SQLite 상태를 관리하고, skills는 연결된 브라우저와 사용자 확인을 통해 작업을 수행합니다.

[통합 포트폴리오 PDF](portfolio/crossborder-portfolio.pdf) · [편집용 PPTX](portfolio/crossborder-portfolio.pptx) · [실험 결과](docs/experiment.md) · [설계와 한계](docs/design.md) · [별도 URL 분석기](https://github.com/y00nZZang/product-catalog)

## 왜 만들었나

직접 구매에는 가격 비교 외에도 판본 확인, 배송지 입력, 주문 정보 이전, 본인확인, 배송 추적이 필요합니다. 한 번의 구매를 직접 관찰한 뒤 반복 입력을 에이전트에 맡기고, 인증·구매 확정과 모호한 결과에는 사용자 개입과 대조 절차를 남겼습니다.

## 현재 범위

| 단계 | 구현 | 검증 상태 |
|---|---|---|
| 상품 탐색 | 판매처 제한 없는 조사 skill, JSON-LD 후보 추출 | 합성 표본 + 실제 Blu-ray 조사 |
| 배송대행 비교 | 3개 업체 조사, 조건·누락·만료 검사 | JPY/KRW helper 검증; USD 환산 미지원 |
| 라쿠텐 북스 | 조건 승인·중복 시도 방지·주문 결과 대조 | 사용자가 최종 구매, 에이전트가 결과 확인 |
| 몰테일 등록 | 현재 주소 확인·신청 작성·동일 초안 재개 | 사용자 통관 인증 후 접수 및 목록 확인 |
| 배송 추적 | 메일/사이트 대조 지침, 조회 이벤트 기록 | helper 테스트만; 발송·수령 미검증 |

**2026-10-05 실거래 1건**에서 주문 합계 5,616엔과 몰테일 접수를 확인했습니다. 무인 구매 성공, 시간 절감률, 배송 완료 또는 최종 총비용을 의미하지 않습니다. 실제 사용에서 치수 없는 견적 거절, USD 환산, 사용자 직접 주문을 ledger로 가져오는 기능의 공백을 발견했습니다.

## 재현

Python 3.10+ 표준 라이브러리만 필요합니다. 아래 명령은 실구매를 하지 않습니다.

```sh
python3 -m unittest discover -s tests -v
python3 plugin/scripts/purchase_agent.py --help
python3 plugin/scripts/purchase_agent.py extract tests/fixtures/product.html --url https://example.com/product
python3 scripts/package_plugin.py
```

패키지: `dist/crossborder-purchase-0.1.0.zip`. Codex plugin을 지원하는 환경에서 로컬 패키지로 등록하거나 `plugin/skills/.../SKILL.md`를 읽도록 요청하세요. 브라우저 도구는 별도로 연결되어 있어야 합니다. 추적 시 Gmail·예약 도구는 선택 사항입니다. 설치 UI는 클라이언트 버전에 따라 달라질 수 있습니다.

처음에는 다음처럼 조사만 실행하세요.

> 이 상품 URL의 판본·가격·재고와 몰테일·tenso·転送JAPAN 견적을 비교해줘. 이번에는 구매나 신청서를 제출하지 마.

실거래는 사용자 확인 후 진행하며 로그인·OTP·통관 인증은 직접 수행합니다. 기본 DB는 `~/.local/share/crossborder-purchase/ledger.sqlite3`; 테스트는 임시 DB를 사용합니다. 실행 상태나 주문 식별자는 커밋하지 마세요.

## 코드 읽기

- `plugin/skills/`: 다섯 단계의 행동 지침과 사용자 개입 경계
- `plugin/scripts/state.py`: 승인 조건, 상태 전이, 중복 실행 방지
- `plugin/scripts/quotes.py`: 동일 조건 비교, 누락 비용·만료 검사
- `plugin/scripts/extract.py`: HTML의 구조화 상품 후보 추출
- `tests/test_plugin.py`: 오프라인 회귀 테스트
- [명령별 입력 계약](plugin/references/runtime.md)

개인 프로젝트이며 SAZO·Rakuten·Malltail의 공식 제품이나 제휴 서비스가 아닙니다. Codex를 구현·실험에 사용했으며 기술·제품 판단과 결과 검토는 프로젝트 작성자가 수행했습니다. 원본 비공개 저장소의 Git 이력을 포함하지 않는 공개용 스냅샷입니다.
