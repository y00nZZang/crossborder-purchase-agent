# 제출 포트폴리오 원고

2026-10-05. 제품·시장 이해와 실제 구매 실험 중심.

## 1

01   윤장한 · 구매대행 제품 실험 · 2026.10.05
PRODUCT ENGINEERING PORTFOLIO
구매대행의 일을 분해하고,
직접 구매와 비용 예측을
제품으로 실험했습니다
구매대행 에이전트  +  URL 기반 배송·관세 추론기
윤장한  ·  개인 프로젝트  ·  2026년 10월 기준

근거: 개인 프로젝트. 구현·실험에 Codex 사용. 제품·기술 판단과 검증 결과 정리는 작성자 수행. 각 결과의 한계는 후속 슬라이드와 공개 문서에 명시.

## 2

구매대행은 어떤 일을 대신하는가
조사·입력의 자동화가 전체 구매 경험의 대체로 이어지는지 확인하고 싶었습니다.
02   윤장한 · 구매대행 제품 실험 · 2026.10.05
구매 과정
사용자가 해결해야 할 문제
실험한 제품
구매 전
판본·총비용·배송 조건을 비교하기 어렵다
URL 분석·비용 추정
주문과 신청
사이트별 주소·주문 정보를 다시 입력한다
Codex 구매대행 plugin
인증과 예외
로그인·본인확인·결과 불일치를 처리한다
사용자 개입과 재개 절차
입고 이후
실측·검수·국제운송·보상 책임이 남는다
이번 실험의 미검증 범위
질문: 에이전트가 줄일 수 있는 업무와, 물류·책임을 가진 사업자에게 남는 가치는 무엇인가?

근거: https://github.com/y00nZZang/crossborder-purchase-agent/blob/main/docs/design.md ; https://github.com/y00nZZang/crossborder-purchase-agent/blob/main/docs/experiment.md

## 3

직접구매가 항상 저렴하지는 않았습니다
2026-09-21 · 같은 Blu-ray의 경로별 부분 견적. 최종 비용 순위나 자동화 절감 실적은 아닙니다.
03   윤장한 · 구매대행 제품 실험 · 2026.10.05
경로
확인 비용 합계
비교 조건과 한계
SAZO
약 7,228엔
63,878원 환산 · 운송사·세부 조건 미확인
라쿠텐 북스 + tenso
7,472엔
250g · 19×14×2cm · EMS 가정
공식 스토어 직배송
약 7,821엔
69,112원 환산 · 특전 차이 가능
라쿠텐 북스 + WorldShopping
8,189엔
250g · EMS 가정 · 대행료 포함
수수료 한 항목보다 총비용의 구성과 미확정 조건을 함께 보여주는 제품이 필요했습니다.
환산 가정: 100엔 = 883.7원. 실측·카드 비용·세금 등 누락 가능. 당시 자료이며 현재 가격이 아닙니다.

근거: https://github.com/y00nZZang/crossborder-purchase-agent/blob/main/docs/route-comparison.md ; https://www.tenso.com/jp/estimate ; https://www.worldshopping.global/simulator/ ; https://books.rakuten.co.jp/rb/18584086/ . 당시 관측·사용자 제공 캡처. SAZO 목록 접힘 및 특전·운송/보상 차이 미해소.

## 4

실제 구매에서 드러난 세 가지 병목
화면의 다음 버튼을 누르는 것보다, 준비 상태와 결과를 확인하는 일이 중요했습니다.
04   윤장한 · 구매대행 제품 실험 · 2026.10.05
인증이 구매 경로를 바꿨습니다
텐소 주소 증빙 보완 요청 이후 몰테일 경로를 선택했습니다.
최초 계정 준비와 반복 구매 업무는 같은 자동화 지표로 볼 수 없었습니다.
입력 완료와 접수 완료가 달랐습니다
통관부호 인증으로 제출이 차단됐습니다. 사용자 인증 후 같은 초안에서 재개하고
접수 화면과 저장 목록을 대조했습니다.
금액과 상태가 시스템 사이에서 달라졌습니다
주문 확인값과 실제 주문 상세에 3엔 차이가 있었습니다. 실제 접수값을 기준으로
배송신청에 반영했으며 차이의 원인은 미확인으로 남겼습니다.

근거: https://github.com/y00nZZang/crossborder-purchase-agent/blob/main/docs/experiment.md ; 2026-09-22 텐소 주소증빙 보완 안내 및 2026-09-29 경로 전환 관측.

## 5

구매대행 에이전트: 실행과 확인을 분리했습니다
다섯 개 skill과 Python helper로, 브라우저 판단·계산·상태 기록의 역할을 나눴습니다.
05   윤장한 · 구매대행 제품 실험 · 2026.10.05
상품 조사 → 견적 비교 → 라쿠텐 구매 → 몰테일 신청 → 배송 추적
Skill은 연결된 브라우저에서 현재 화면을 읽고 작업합니다.
고정 셀렉터 기반의 무인 구매 봇이나 상시 서버는 아닙니다.
승인한 조건과 실행 시도를 SQLite에 기록합니다
Python helper가 조건 digest·상태 전이·중복 시도를 검사합니다.
모호한 결과는 재주문보다 기존 주문·신청 목록 확인을 우선합니다.
사용자에게 남긴 판단과 개입
로그인·추가 인증·최종 구매는 사용자가 수행했습니다.
외부 거래와 로컬 ledger가 원자적으로 일치하는 구조는 아닙니다.

근거: https://github.com/y00nZZang/crossborder-purchase-agent/blob/main/docs/design.md ; https://github.com/y00nZZang/crossborder-purchase-agent/tree/main/plugin

## 6

실제 주문과 배송대행 접수를 확인했습니다
2026-10-05 · 별도 세션의 짧은 요청으로 시험한 단일 사례
06   윤장한 · 구매대행 제품 실험 · 2026.10.05
FJORD 통상판 Blu-ray 1개
상품 5,666엔 − 쿠폰 50엔
일본 배송비 0엔
주문 합계 5,616엔
사용자: 로그인·최종 구매·통관 인증
에이전트: 조사·입력·주문 대조·신청 접수
국제운임·발송·한국 수령은 미확인입니다.
성공률·시간 절감률은 측정하지 않았습니다.

근거: https://github.com/y00nZZang/crossborder-purchase-agent/blob/main/docs/experiment.md . 완료 캡처는 사용자 제공 실험 산출물. 주문식별자와 개인 주소는 공개하지 않음.

## 7

구매 전 불확실성을 줄이는 URL 분석기
상품명·가격만으로는 한국 도착 비용을 비교하기 어려워 별도 서비스를 구현했습니다.
07   윤장한 · 구매대행 제품 실험 · 2026.10.05
사용자 입력은 상품 URL 하나로 줄였습니다
수집 → 배송 정보 추정 → 관세 정보 추정의 서버 진행 상태를 표시합니다.
요약을 먼저 보여주고 출처·가정·계산 조건은 상세에서 확인하게 했습니다.
판매처마다 다른 수집 경로를 연결했습니다
라쿠텐 이치바·북스 API, 공개 HTML, 필요한 경우 브라우저를 사용합니다.
메루카리의 개별 판매글을 식별하며 다른 판매글을 임의로 병합하지 않습니다.
불확실한 비용을 0으로 숨기지 않았습니다
관측값·모델 가정·미확인 항목을 분리하고 부분 견적을 유지합니다.
구매대행 plugin과는 현재 독립 프로젝트이며 자동 거래로 연결하지 않았습니다.

근거: https://github.com/y00nZZang/product-catalog/blob/main/README.md ; https://github.com/y00nZZang/product-catalog/blob/main/docs/architecture.md

## 8

URL 입력부터 비용 요약까지
운영 데모의 실제 결과 · 추정치를 확정 견적처럼 표시하지 않습니다.
08   윤장한 · 구매대행 제품 실험 · 2026.10.05

근거: https://github.com/y00nZZang/product-catalog/blob/main/docs/verification.md ; https://catalog.janghan.dev/ ; 2026-10-05 실제 운영 캡처의 상단 일부.

## 9

모델 추론과 계산 규칙의 경계를 정했습니다
누락 정보를 보완하되, 그럴듯한 숫자가 확인값으로 바뀌지 않게 했습니다.
09   윤장한 · 구매대행 제품 실험 · 2026.10.05
문제
구현한 대응
결과를 해석하는 경계
포장 사양 부족
이미지·제품명·웹 검색으로 무게·세 변 추정
실측과 모델 가정 구분, 범위·근거 검사
자연어 상품 분류
규칙과 LLM으로 HS → HSK 후보 선택
품목분류 법적 확정 아님
세율 미등록
공개 HSK 기본세율 조회, 기간·추가세 검사
FTA·WTO 조건을 임의 적용하지 않음
세액 산술
고정소수점 계산, 주류 별도 프로필
추가 세목·입력 부족은 보류
카드 사례: HSK 9504400000 · 기본관세 8% + 일반 부가세 10% 가정
예상 세금 115,776~117,335원 — 실제 납부세액과 대조한 결과는 아닙니다.

근거: https://github.com/y00nZZang/product-catalog/blob/main/docs/public-hsk-rates-2026-10-05.md ; https://github.com/y00nZZang/product-catalog/tree/main/src/ai ; https://unipass.customs.go.kr/clip/hsinfosrch/openULS0401009Q.do

## 10

중복 요청과 워커 실패 처리
NestJS API · PostgreSQL 큐/캐시 · 독립 수집 워커 · Linux 컨테이너
10   윤장한 · 구매대행 제품 실험 · 2026.10.05
같은 판매글 요청은 공유하고, 만료된 관측만 갱신합니다
플랫폼·판매글 ID·옵션을 키로 사용합니다. 라쿠텐 6시간·메루카리 1시간 TTL,
AI 요청 캐시와 DB 잠금으로 중복 수집·호출을 줄입니다.
워커가 멈춰도 결과를 중복 저장하지 않도록 검사합니다
작업 임대와 복구, 오래된 워커 쓰기 방지, 제한된 재시도·요청 간격을 둡니다.
입력 URL과 리디렉션에 내부망 접근 방지를 적용합니다.
실행시간과 비용을 결과 데이터에서 분리합니다
analysis_runs·analysis_steps에 단계·시도·캐시·오류를 기록합니다.
캐시 적중 요청에 과거 분석시간을 이번 처리시간으로 재사용하지 않습니다.

근거: https://github.com/y00nZZang/product-catalog/blob/main/docs/architecture.md ; https://github.com/y00nZZang/product-catalog/tree/main/src/persistence ; https://github.com/y00nZZang/product-catalog/tree/main/src/jobs

## 11

검증 결과와 남은 과제
테스트 개수는 동작 회귀의 근거이며, 예측 정확도나 운영 SLA가 아닙니다.
11   윤장한 · 구매대행 제품 실험 · 2026.10.05
범위
확인 결과
남은 검증
구매대행 helper
오프라인 테스트 25개 통과
외부 주문 import·USD·치수 없는 견적
실제 구매 실험
사용자 구매 후 몰테일 접수 1건
발송·실측 운임·수령·반복 표본
분석기 코드·DB
회귀 298개 + 통합 17개 통과
장기 운영·복구 훈련·부하별 비용
배송·관세 추정
라이브 흐름과 공개 세율 연결 확인
실측 포장·실제 납부세액 오차
표본의 일부는 에이전트 검토 자료입니다. 독립적인 사람 이중 검수 정답셋으로 표현하지 않습니다.

근거: https://github.com/y00nZZang/crossborder-purchase-agent/blob/main/docs/experiment.md ; https://github.com/y00nZZang/product-catalog/blob/main/docs/verification.md . 공개 독립 checkout에서 2026-10-05 재실행.

## 12

제품·시장에 대한 현재 해석
한 사례에서 확인한 자동화 가능성을 시장 전체의 대체 효과로 확대하지 않았습니다.
12   윤장한 · 구매대행 제품 실험 · 2026.10.05
관찰: 정보 이전과 반복 입력은 에이전트가 보조할 수 있습니다
다만 인증·최종 구매·모호한 금액의 대조가 남았습니다.
자동화 수준과 사용자가 결과를 확인하는 부담을 함께 봐야 합니다.
제품 판단: 비용의 예측 가능성과 근거를 먼저 개선했습니다
URL만 입력하는 분석 흐름을 만들고, 확인한 비용과 남은 조건을 함께 표시했습니다.
계산 보류를 억지 성공으로 바꾸기보다 부족한 이유를 드러냈습니다.
가설: 물류·검수·보상과 예외 대응이 차별점으로 남을 수 있습니다
물량 집약 운임이나 구매대행 사업자의 내부 원가는 확인하지 못했습니다.
소비자 견적 차이만으로 경쟁력의 원인을 단정하지 않습니다.

근거: https://github.com/y00nZZang/crossborder-purchase-agent/blob/main/docs/design.md ; https://github.com/y00nZZang/crossborder-purchase-agent/blob/main/docs/route-comparison.md ; https://github.com/y00nZZang/product-catalog/blob/main/docs/verification.md

## 13

다음 검증과 공개 산출물
문제 관찰 → 제품 결정 → 구현 → 검증의 근거를 코드와 문서로 연결했습니다.
13   윤장한 · 구매대행 제품 실험 · 2026.10.05
다음 검증: 같은 조건의 반복 구매와 실제 청구값 대조
사람의 개입 횟수·재입력·복구 여부를 기록하고, 포장 실측·배송 청구액·세액과
예측값을 비교해야 합니다. 이 결과가 확보되기 전 절감률을 주장하지 않습니다.
구매대행 에이전트
https://github.com/y00nZZang/crossborder-purchase-agent
URL 분석·배송·관세 추론기
https://github.com/y00nZZang/product-catalog
데모  https://catalog.janghan.dev/
기획·조사·구현·배포·실험 정리: 윤장한  /  구현 보조: Codex

근거: https://github.com/y00nZZang/crossborder-purchase-agent ; https://github.com/y00nZZang/product-catalog ; https://catalog.janghan.dev/
