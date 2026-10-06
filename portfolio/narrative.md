# 직구 과정 조사와 두 가지 도구 구현

2026-10-06 개정. 도구와 사업의 미확인 범위, 개인적 생각을 구분.

## 1


01   윤장한 · 직구 조사와 도구 구현 · 2026.10.06
개인 프로젝트 · 윤장한
직구 과정 조사와
두 가지 도구 구현
Codex 플러그인 · 상품 URL 분석기
검증 질문, 관찰한 내용, 구현과 시험 결과

근거: 개인 프로젝트. 기획·조사·검증과 도구 구현에 Codex 사용. 관측과 테스트 결과는 2026-10-05 기준, 문서 개정 2026-10-06.

## 2

검증하고자 한 내용
직접 구매 과정과, 해외 사이트 결제 이후에 추가되는 비용을 살펴봤습니다.
02   윤장한 · 직구 조사와 도구 구현 · 2026.10.06
구매 과정
개인이 에이전트의 도움을 받아
상품 조사·주문·배송신청·통관을
어디까지 진행할 수 있는가?
구매 전 정보
해외 사이트에서 구매한 뒤
추가로 발생하는 국제운송비와 관세를
어떻게 추정할 수 있을까?
실제 시험은 주문 확인·배송대행 접수까지 진행했습니다. 통관 완료는 아직 관측하지 않았습니다.

근거: https://github.com/y00nZZang/crossborder-purchase-agent/blob/main/docs/design.md ; https://github.com/y00nZZang/product-catalog/blob/main/README.md . 통관은 추적·비용 추정의 관심 범위이며 실제 통관 완료는 미검증.

## 3

직구 과정에서 확인한 불편
가격을 비교하는 것 외에도 가입·인증·입력과 확인이 필요했습니다.
03   윤장한 · 직구 조사와 도구 구현 · 2026.10.06
과정
겪거나 확인한 내용
가입·이용 준비
메루카리는 해외 거주자로 직접 가입·구매하기 어려웠음
tenso는 주소 증빙 보완·재제출 과정이 번거롭게 느껴졌음
비용 비교
포장 규격·무게가 없고 운임·수수료 조건이 달라 비교가 어려웠음
주문·배송신청
이커머스와 배송대행 사이트에 정보를 옮기고 접수 결과를 대조해야 했음
진행 확인
인증을 마친 뒤 재개하거나 메일·사이트에서 다음 상태를 확인해야 했음
이번 직접 구매 시험은 라쿠텐 북스와 몰테일 경로로 진행했습니다.

근거: https://github.com/y00nZZang/crossborder-purchase-agent/blob/main/docs/experience-notes.md ; https://github.com/y00nZZang/crossborder-purchase-agent/blob/main/docs/experiment.md . 특정 개인 경험이며 모든 해외 사용자에 대한 현행 정책 단정 아님.

## 4

구매 경로별 부분 견적
2026-09-21 · 영상 매체(Blu-ray) 1개를 기준으로 조사했습니다.
04   윤장한 · 직구 조사와 도구 구현 · 2026.10.06
경로
확인 비용 합계
조건
SAZO
약 7,228엔
63,878원 환산 · 세부 조건 미확인
라쿠텐 북스 + tenso EMS
7,472엔
250g · 19×14×2cm 가정
공식 스토어 + EMS
약 7,821엔
69,112원 환산 · 특전 차이 가능
라쿠텐 북스 + WorldShopping EMS
8,189엔
250g 가정 · 대행료 포함
비교 시 비용 합계뿐 아니라 포장·운송·특전 조건도 함께 확인해야 했습니다.
100엔=883.7원으로 환산. 당시 부분 견적이며 실측·카드 비용·세금 등은 미확정입니다.

근거: https://github.com/y00nZZang/crossborder-purchase-agent/blob/main/docs/route-comparison.md ; https://www.tenso.com/jp/estimate ; https://www.worldshopping.global/simulator/ ; https://books.rakuten.co.jp/rb/18584086/ . SAZO 사용자 제공 캡처, 세부 운송·특전 조건 미확인.

## 5

소량 구매의 배송비에 대한 생각
작고 가벼운 상품을 한 개 구매할 때 배송비의 부담이 크게 느껴졌습니다.
05   윤장한 · 직구 조사와 도구 구현 · 2026.10.06
관찰과 체감
최소 과금 구간에 해당하는 소형 상품은
무게가 더 작아도 배송비가 비례해서
줄지는 않을 수 있다고 생각했습니다.
단품 구매에서는 상품 크기에 비해
배송비가 크게 느껴졌습니다.
확인해보고 싶은 가설
여러 상품을 한 포장으로 보내면
기본 배송비를 나누어 부담할 수 있어
개당 비용이 줄어들 수 있지 않을까?
개별 발송 합계 ↔ 합배송 총액
운임 + 합포장·처리·보관 비용을 비교
합배송 이익은 아직 검증하지 않았습니다. 합친 무게·부피와 추가 수수료에 따라 달라질 수 있습니다.

근거: https://github.com/y00nZZang/crossborder-purchase-agent/blob/main/docs/experience-notes.md ; https://github.com/y00nZZang/crossborder-purchase-agent/blob/main/docs/route-comparison.md . 사용자 체감과 합배송 가설. 실제 합배송 실측·절감액 미검증.

## 6

만들어본 두 가지 도구
구매 실행을 보조하는 도구와, 구매 전 정보를 분석하는 도구를 별도로 구현했습니다.
06   윤장한 · 직구 조사와 도구 구현 · 2026.10.06
01  Codex 플러그인
조사·입력·상태 확인 보조
상품 조사와 배송대행 비교
이커머스 주문 대조·배송대행 신청
구매 확인 후 일일 메일 추적 등록
02  URL 분석기
상품·배송·관세 정보 추정
판매처별 상품 정보 수집
이미지·검색 기반 포장 사양 추정
공개 세율을 이용한 예상 세금 계산
두 도구는 독립적으로 동작합니다. 플러그인의 실제 실행 경로는 일부 서비스에서 검증했습니다.

근거: https://github.com/y00nZZang/crossborder-purchase-agent/blob/main/README.md ; https://github.com/y00nZZang/product-catalog/blob/main/README.md . 플러그인 실제 검증 경로는 라쿠텐 북스·몰테일. 일반 명칭은 역할 설명이며 범용 사이트 지원 의미 아님.

## 7

Codex 플러그인 구성
다섯 개 skill이 작업 절차를 안내하고, Python helper가 계산과 상태를 관리합니다.
07   윤장한 · 직구 조사와 도구 구현 · 2026.10.06
상품 조사
배송대행 비교
이커머스 구매
배송대행 신청
진행 추적
브라우저와 skills
현재 상품·폼·완료 화면을 확인하고 입력
Python + SQLite
승인 조건·실행 시도·견적·상태 기록
사용자
로그인·추가 인증·최종 구매 수행
현재 실행 검증: 라쿠텐 북스 구매·몰테일 신청. 다른 서비스로의 확대는 별도 구현이 필요합니다.

근거: https://github.com/y00nZZang/crossborder-purchase-agent/tree/main/plugin ; https://github.com/y00nZZang/crossborder-purchase-agent/blob/main/docs/design.md . 실제 구현 어댑터 라쿠텐 북스·몰테일.

## 8

Codex 플러그인 시험 결과
상품 URL과 목적을 전달한 뒤 확인·승인 중심으로 진행했습니다. 아래 대화는 실제 기록을 축약했습니다.
08   윤장한 · 직구 조사와 도구 구현 · 2026.10.06
첫 요청 1회 + 후속 입력 6회
나 · 입력 순서
에이전트 · 안내와 처리 결과
① URL + 구매·배송신청 요청
상품 확인 → 로그인 안내
②·③ 각 사이트 로그인 완료
배송지 확인 → 정보 입력 승인 요청
④ 주소 입력 승인 + 무게 조건 보완
주소 입력·견적 비교 → 구매 확정 안내
⑤ 직접 구매 완료 알림
주문 대조·신청서 작성 → 제출 확인
⑥ 제출 진행 승인
제출 시도 → 통관 인증 안내
⑦ 인증 완료 알림
동일 신청서 제출 → 접수 완료 확인
사용자 메시지 기준의 단일 사례입니다. 로그인·구매·인증 화면의 클릭·입력 횟수는 별도이며 미측정입니다.

근거: https://github.com/y00nZZang/crossborder-purchase-agent/blob/main/docs/interaction-count.md ; https://github.com/y00nZZang/crossborder-purchase-agent/blob/main/docs/experiment.md . 사용자 메시지7개. 로그인 두 번을 한 행으로 묶은 요약이며 실제 원문 대화 캡처가 아님.

## 9

구매 확인 후 일일 메일 추적
구매 완료가 확인되면 Codex scheduler에 하루 한 번의 추적 작업을 등록합니다.
09   윤장한 · 직구 조사와 도구 구현 · 2026.10.06
구매 완료 확인
일일 scheduler 등록
주문·배송 진행 추적
실제 주문 접수 근거 확인
배송대행 접수 전에도 시작
메일 단회 조회 후 등록
기존 예약 ID가 있으면 재사용
주문·배송대행 메일 확인
발송·입고·출고·통관 상태 대조
의미 있는 변경이나 사용자 조치가 필요할 때 알리고,
배송완료·취소가 확인되면 예약을 종료합니다.

근거: https://github.com/y00nZZang/crossborder-purchase-agent/blob/main/plugin/skills/crossborder-track-delivery/SKILL.md ; https://github.com/y00nZZang/crossborder-purchase-agent/blob/main/docs/daily-tracking.md . 2026-10-06 v0.1.1 동작 변경. 실거래 당시 동작과 구분.

## 10

URL 분석기 · 실행 화면
https://catalog.janghan.dev/  ·  URL 입력 → 상품 수집 → 배송·관세 추정
10   윤장한 · 직구 조사와 도구 구현 · 2026.10.06

근거: https://github.com/y00nZZang/product-catalog/blob/main/docs/verification.md ; https://catalog.janghan.dev/ . 2026-10-06 캡처, 10/5 저장 관측 결과. 동일 페이지의 입력·결과 영역을 나누어 배치.

## 11

URL 분석기의 처리 과정
라쿠텐 이치바·북스와 메루카리의 상품 URL을 입력으로 사용합니다.
11   윤장한 · 직구 조사와 도구 구현 · 2026.10.06
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

## 12

관세 실험 결과
동일한 항목으로 정리하되, 실제 URL 분석과 합성 계산 표본의 차이는 구분했습니다.
12   윤장한 · 직구 조사와 도구 구현 · 2026.10.06
항목
TCG 상품
주류(위스키)
검증 자료
메루카리 실제 판매글
2026-10-05 운영 분석
제조사 사양 + 합성 계산 입력
2026-09-30 저장 시험
분류·추출 결과
HSK 9504400000 후보
whisky 후보 · 700ml·43% 추출
병 수는 미확인
계산 조건
관측 판매가70,000JPY
기본관세8%·일반 부가세10% 가정
별도 합성 입력: $200·750ml 1병·40%
환율1,000원/$·운임0 가정
예상 세금
115,776 ~ 117,335원
353,696원
확인한 범위
상품 분류→공개 세율→계산 연결
사양 추출과 계산 회귀
용량·병 수 경계 및 누락 입력 검사
실제 납부세액과 대조한 정확도 검증은 아닙니다. 주류의 사양 추출 표본과 산술 표본은 서로 다릅니다.

근거: https://github.com/y00nZZang/product-catalog/blob/main/docs/alcohol-test-evidence.md ; https://github.com/y00nZZang/product-catalog/blob/main/docs/verification.md . TCG 10/5 운영 결과와 주류9/30 제조사 사양 추출/합성 계산은 별도 시험.

## 13

도구 측면에서 남은 질문
이번 구현으로 확인하지 못한 범위입니다. 추가 개발·검증 일정은 잡지 않았습니다.
13   윤장한 · 직구 조사와 도구 구현 · 2026.10.06
영역
확인하지 못한 부분
추정 정확도
포장 치수·무게와 관세 추정이 실제 값과 얼마나 일치하는가
인형처럼 형태가 복잡한 상품도 적절한 포장 범위를 추정하는가
판매처 확대
라쿠텐·메루카리 밖의 사이트에서도 안정적으로 수집·파싱할 수 있는가
API가 없는 사이트의 화면 변경·접근 제한에 어떻게 대응할 것인가
라쿠텐은 API로 상품 정보를 가져왔습니다.
메루카리는 웹페이지를 크롤링하고 HTML을 파싱했습니다.

근거: https://github.com/y00nZZang/product-catalog/blob/main/docs/verification.md ; https://careers.mercari.com/mercan/articles/47692/ . 2024-11-15 공식 인터뷰의 해외 파트너 API 시스템 연동 사례. 이 프로젝트의 접근 권한 획득/사용 의미 아님.

## 14

이번 경험과 구매대행 사업에 대한 질문
입력 과정의 간소화와 배송비의 경제성은 별도로 보게 됐습니다.
14   윤장한 · 직구 조사와 도구 구현 · 2026.10.06
이번 사례에서 느낀 점
에이전트로 배송대행 정보 입력과
접수 확인을 간소화할 수 있었습니다.

소형·경량 상품1개에서는 직접구매의
비용 이점을 확인하지 못했습니다.
사업 측면에서 남은 질문
합배송으로 운송비를
얼마나 최적화할 수 있을까?

개별 발송과 합배송의 총비용을
포장·처리·보관 비용까지 비교해야 합니다.
당시 확인 비용 합계는 SAZO 약7,228엔, 직접구매+tenso 7,472엔이었습니다.
이 사례에서는 구매대행을 이용하는 편이 유리하다고 느꼈습니다.
운송·특전 등 조건 차이와 미확정 비용이 남아 있어 모든 소량 직구의 결론으로 일반화하지 않습니다.

근거: https://github.com/y00nZZang/crossborder-purchase-agent/blob/main/docs/route-comparison.md ; https://github.com/y00nZZang/crossborder-purchase-agent/blob/main/docs/interaction-count.md . SAZO와 직접구매의 조건 차이가 남는 단일 부분 견적.

## 15

에이전트 커머스에 대한 생각
이번에는 브라우저를 통해 배송대행 정보를 입력했습니다.
15   윤장한 · 직구 조사와 도구 구현 · 2026.10.06
에이전트로 구매가 가능해지고, 배송대행 업체가 신청용 MCP 등을 제공한다면
직구 과정 전체를 에이전트에 맡기는 흐름도 가능하지 않을까 생각했습니다.
에이전트가 구매
배송대행 MCP로 신청
주문·배송·통관 추적
그때 사조 같은 구매대행 업체의 경쟁력은 구매 과정의 간편함뿐 아니라,
합배송으로 비용을 조정하고 물류·검수·예외를 처리하는 노하우에
더 크게 남지 않을까 생각합니다.
공개 코드  github.com/y00nZZang/crossborder-purchase-agent  ·  github.com/y00nZZang/product-catalog

근거: https://github.com/y00nZZang/crossborder-purchase-agent/blob/main/docs/closing-perspective.md . 사용자 의견·미래 가정이며 현재 제공되는 MCP나 사업 경쟁력의 검증 결과가 아님.
