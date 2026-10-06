# 구매대행 과정 조사와 두 가지 도구 구현

문서 개정 2026-10-06. 관측·시험 결과는 2026-10-05 기준.

## 1

01   윤장한 · 구매대행 조사와 도구 구현 · 2026.10.06
개인 프로젝트 · 윤장한
구매대행 과정 조사와
두 가지 도구 구현
Codex 플러그인 · 상품 URL 분석기
검증 질문, 관찰한 내용, 구현과 시험 결과

근거: 개인 프로젝트. 기획·조사·검증과 도구 구현에 Codex 사용. 관측과 테스트 결과는 2026-10-05 기준, 문서 개정 2026-10-06.

## 2

검증하고자 한 내용
구매 과정과 비용 정보를 직접 확인하고, 에이전트가 보조할 수 있는 범위를 살펴봤습니다.
02   윤장한 · 구매대행 조사와 도구 구현 · 2026.10.06
구매 과정
개인이 에이전트의 도움을 받아
상품 조사·주문·배송신청을
어디까지 진행할 수 있는가?
구매 전 정보
상품 URL에 있는 정보로
배송과 관세 비용을
어느 범위까지 추정할 수 있는가?
구매대행의 역할 변화는 탐색 질문으로 두고, 선택한 상품과 경로에서 먼저 시험했습니다.

근거: https://github.com/y00nZZang/crossborder-purchase-agent/blob/main/docs/design.md ; https://github.com/y00nZZang/product-catalog/blob/main/README.md . 최초 연구 목표와 구현 범위를 구분.

## 3

조사와 구매 과정에서 확인한 내용
경로별 견적 비교와 실제 구매를 구분해 기록했습니다.
03   윤장한 · 구매대행 조사와 도구 구현 · 2026.10.06
과정
확인한 내용
도구에 반영한 부분
경로 비교
상품값 외에 운임·취급료·조건 확인 필요
비용 항목과 미확인 조건 표시
이용 준비
계정·주소 증빙·추가 인증 필요
사용자 확인 후 재개하는 절차
주문·배송신청
주소·주문 정보 입력과 결과 대조 필요
기존 주문 확인, 신청 상태 기록
비용 추정
포장 사양·상품 분류가 부족한 경우 존재
검색·모델 보완과 추정 근거 표시
입고 이후의 실측·국제운송·수령은 아직 확인하지 못했습니다.

근거: https://github.com/y00nZZang/crossborder-purchase-agent/blob/main/docs/experiment.md ; https://github.com/y00nZZang/crossborder-purchase-agent/blob/main/docs/route-comparison.md

## 4

구매 경로별 부분 견적
2026-09-21 · FJORD 통상판 Blu-ray 1개를 기준으로 조사했습니다.
04   윤장한 · 구매대행 조사와 도구 구현 · 2026.10.06
경로
확인 비용 합계
조건
SAZO
약 7,228엔
63,878원 환산 · 세부 조건 미확인
북스 + tenso EMS
7,472엔
250g · 19×14×2cm 가정
공식 스토어 EMS
약 7,821엔
69,112원 환산 · 특전 차이 가능
북스 + WorldShopping EMS
8,189엔
250g 가정 · 대행료 포함
비교 시 비용 합계뿐 아니라 포장·운송·특전 조건도 함께 확인해야 했습니다.
100엔=883.7원으로 환산. 당시 부분 견적이며 실측·카드 비용·세금 등은 미확정입니다.

근거: https://github.com/y00nZZang/crossborder-purchase-agent/blob/main/docs/route-comparison.md ; https://www.tenso.com/jp/estimate ; https://www.worldshopping.global/simulator/ ; https://books.rakuten.co.jp/rb/18584086/ . SAZO 사용자 제공 캡처, 세부 운송·특전 조건 미확인.

## 5

만들어본 두 가지 도구
구매 실행을 보조하는 도구와, 구매 전 정보를 분석하는 도구를 별도로 구현했습니다.
05   윤장한 · 구매대행 조사와 도구 구현 · 2026.10.06
01  Codex 플러그인
조사·입력·상태 확인 보조
상품 조사와 배송대행 비교
라쿠텐 주문 대조와 몰테일 신청
사용자 확인·인증 후 작업 재개
02  URL 분석기
상품·배송·관세 정보 추정
판매처별 상품 정보 수집
이미지·검색 기반 포장 사양 추정
공개 세율을 이용한 예상 세금 계산
현재 두 도구는 독립적으로 동작합니다. 자동 주문까지 연결한 통합 서비스는 아닙니다.

근거: https://github.com/y00nZZang/crossborder-purchase-agent/blob/main/README.md ; https://github.com/y00nZZang/product-catalog/blob/main/README.md . 두 도구는 현재 자동 API 연동되지 않음.

## 6

Codex 플러그인 구성
다섯 개 skill이 작업 절차를 안내하고, Python helper가 계산과 상태를 관리합니다.
06   윤장한 · 구매대행 조사와 도구 구현 · 2026.10.06
상품 조사
배송대행 비교
라쿠텐 구매
몰테일 신청
배송 추적
브라우저와 skills
현재 상품·폼·완료 화면을 확인하고 입력
Python + SQLite
승인 조건·실행 시도·견적·상태 기록
사용자
로그인·추가 인증·최종 구매 수행
배송 추적은 절차와 helper를 구현했으며, 실제 발송·수령 검증은 남아 있습니다.

근거: https://github.com/y00nZZang/crossborder-purchase-agent/tree/main/plugin ; https://github.com/y00nZZang/crossborder-purchase-agent/blob/main/docs/design.md

## 7

Codex 플러그인 시험 결과
2026-10-05 · 별도 세션에서 라쿠텐 북스 구매와 몰테일 신청을 진행했습니다.
07   윤장한 · 구매대행 조사와 도구 구현 · 2026.10.06
확인한 결과
Blu-ray 1개 주문 결과 대조
몰테일 접수 화면과 저장 목록 확인
주문 합계 5,616엔
과정에서 확인한 보완점
치수 없는 견적·USD 환산 처리
사용자 직접 주문의 상태 가져오기
최종 구매·인증은 사용자 수행. 1건의 시험이며 국제운임·수령·시간 절감은 미검증입니다.

근거: https://github.com/y00nZZang/crossborder-purchase-agent/blob/main/docs/experiment.md . 사용자 제공 접수 캡처는 개인정보 없는 부분만 사용, 원본 우측 잘림 유지.

## 8

URL 분석기의 처리 과정
라쿠텐 이치바·북스와 메루카리의 상품 URL을 입력으로 사용합니다.
08   윤장한 · 구매대행 조사와 도구 구현 · 2026.10.06
상품 정보 수집
배송 정보 추정
관세 정보 추정
API·HTML·브라우저
상품명·가격·판매 상태
이미지·제품명·검색
포장 무게·치수·운임
HS·HSK 후보와 공개 세율
환율·조건별 예상 세금
실시간 진행 상태와 단계별 결과를 표시하고, 상세에서 출처와 추정 조건을 확인합니다.
수집값·모델 가정·미확인 항목을 구분하며, 입력 부족이나 조회 실패는 부분 결과로 남깁니다.

근거: https://github.com/y00nZZang/product-catalog/blob/main/README.md ; https://github.com/y00nZZang/product-catalog/blob/main/docs/architecture.md

## 9

URL 분석기 결과 화면
2026-10-05 운영 화면 · 상품·배송·세금 요약과 미확인 조건을 함께 표시합니다.
09   윤장한 · 구매대행 조사와 도구 구현 · 2026.10.06

근거: https://github.com/y00nZZang/product-catalog/blob/main/docs/verification.md ; https://catalog.janghan.dev/ . 기존 관측 결과 화면, 실측·실제 납부 세액 아님.

## 10

추론과 계산의 처리 기준
판매처 정보만으로 부족한 항목을 보완하되, 확인값과 추정값을 구분합니다.
10   윤장한 · 구매대행 조사와 도구 구현 · 2026.10.06
항목
처리 방식
결과에 남기는 정보
포장 무게·치수
상품 이미지·검색·LLM으로 범위 추정
출처·모델 가정·확인 필요 항목
상품 분류
규칙·LLM으로 HS → HSK 후보 선택
후보 코드·선택 근거
세금
공개 기본세율 조회 후 규칙으로 계산
세율 출처·기간·미적용 조건
카드 시험: HSK 9504400000 · 기본관세 8% + 일반 부가세 10% 가정
예상 세금 115,776~117,335원
FTA·WTO 조건을 임의 적용하지 않습니다. 포장 실측·실제 납부세액과의 대조는 남아 있습니다.

근거: https://github.com/y00nZZang/product-catalog/blob/main/docs/public-hsk-rates-2026-10-05.md ; https://github.com/y00nZZang/product-catalog/tree/main/src/ai ; https://unipass.customs.go.kr/clip/hsinfosrch/openULS0401009Q.do

## 11

구현 확인과 추가 검증
2026-10-05 공개본에서 실행한 테스트와 실제 시험의 범위를 구분했습니다.
11   윤장한 · 구매대행 조사와 도구 구현 · 2026.10.06
대상
확인한 범위
남은 검증
Codex 플러그인
helper 25개 테스트 · 신청 접수 1건
외부 주문 가져오기·배송 추적
URL 분석기
회귀 298개 · DB 통합 17개 테스트
실제 프로세스 중단·장기 운영
배송·관세 추정
실제 URL과 공개 세율 연결
포장 실측·청구액·실제 세액 오차
분석기에는 동시 요청 공유·TTL 캐시·작업 임대·실행시간 기록을 구현했습니다.
테스트 통과 수는 예측 정확도나 사용자 작업시간 개선을 의미하지 않습니다.

근거: https://github.com/y00nZZang/crossborder-purchase-agent/blob/main/docs/experiment.md ; https://github.com/y00nZZang/product-catalog/blob/main/docs/verification.md

## 12

현재까지 확인한 내용과 다음 검증
구매 업무 보조와 비용 정보 추정의 실행 가능성을 각각 확인했습니다.
12   윤장한 · 구매대행 조사와 도구 구현 · 2026.10.06
확인한 내용
사용자 인증·최종 구매를 포함해
주문 대조와 배송신청을 진행했습니다.
URL의 상품 정보에 추정을 더해
배송·세금 시나리오를 반환했습니다.
다음에 확인할 내용
반복 구매에서 개입·재입력·확인 부담
실측 포장·실제 청구값과의 차이
이 결과를 바탕으로 도구의 유용성과
구매대행에 남는 역할을 검토합니다.
코드  github.com/y00nZZang/crossborder-purchase-agent
코드  github.com/y00nZZang/product-catalog     데모  catalog.janghan.dev
기획·조사·구현·검증 정리: 윤장한  /  구현 보조: Codex

근거: https://github.com/y00nZZang/crossborder-purchase-agent/blob/main/docs/experiment.md ; https://github.com/y00nZZang/product-catalog/blob/main/docs/verification.md
