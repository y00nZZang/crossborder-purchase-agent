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

구매 경로별 비용 구성
2026-10-06 확인 · 영상 매체(Blu-ray) 1개 · 원화 비교 환산
04   윤장한 · 직구 조사와 도구 구현 · 2026.10.06
구매 경로
커머스 구매 비용¹
배송 비용²
별도 표시
확인 소계
SAZO
50,363원
7,715원
5,036원³
63,114원
라쿠텐 북스 + tenso EMS
약48,802원
(5,666엔)
약15,504원
(1,800엔)
추가비 별도
약64,306원
라쿠텐 북스 + 몰테일 항공
약48,371원
(주문5,616엔)
약21,212원
($15.63)
추가비 별도
약69,583원
라쿠텐 북스 + WorldShopping EMS
약53,682원
(상품+대행료10%)
약16,796원
(1,950엔)
추가비 별도
약70,478원
공식 스토어 + 국제배송
51,868원
14,419원
추가비 별도
66,287원
¹ 몰테일 경로는50엔 쿠폰 적용 주문. WorldShopping은 대행료 포함. ² 운임·취급료 포함. 공식 스토어 운송사 미표기.
³ SAZO의 ‘통관·관세’ 표시 항목. tenso·WorldShopping은250g·19×14×2cm, 몰테일은0.5kg 최저 구간 가정.
환산: 1엔=8.6131원·1달러=1,357.14원(10/4~10 과세환율). 실측·보험·세금·카드비용에 따라 달라질 수 있습니다.

근거: https://github.com/y00nZZang/crossborder-purchase-agent/blob/main/docs/route-comparison-2026-10-06.md . 가격과 환율·가정은 동일 문서 참조. SAZO 결제 전 견적, 라쿠텐 상품페이지·주문메일, tenso/WorldShopping 계산기, 몰테일 공개요율을 대조. 공식스토어는 사용자 제공10/6 결제 전 캡처: 상품51,868원+배송14,419원=66,287원. 첨부에는 EMS 등 운송방식 미표기. 원화 환산은 카드 청구액 아님.

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
첫 요청 1회 + 후속 입력 6회로 배송대행 접수까지 진행했습니다.
08   윤장한 · 직구 조사와 도구 구현 · 2026.10.06
이 상품을 구매하고
배송대행 신청까지 진행해줘
나
상품·배송 조건 확인 후
로그인과 정보 입력 승인을 요청
에이전트
로그인 완료 · 입력/제출 승인
구매/인증 완료 알림
나
주문 정보를 대조하고 신청서 작성
인증 후 같은 신청서로 접수 완료
에이전트
실제 접수 결과
대화는 실제 기록의 요약입니다. 후속 입력은 로그인2회·승인2회·구매/인증 완료 알림2회입니다.
메시지 수 기준이며, 로그인·구매·인증 화면의 클릭과 입력 횟수는 별도로 측정하지 않았습니다.

근거: https://github.com/y00nZZang/crossborder-purchase-agent/blob/main/docs/interaction-count.md ; https://github.com/y00nZZang/crossborder-purchase-agent/blob/main/docs/experiment.md . 실제 대화 요약. 로그인2회·승인2회·구매/인증 완료2회를 묶어 표현. 사용자 첨부 대화 스타일 참고, 실제 접수 캡처 유지.

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
https://catalog.janghan.dev/
10   윤장한 · 직구 조사와 도구 구현 · 2026.10.06
URL 입력
상품 링크 하나로
분석을 시작합니다.
결과 확인
상품·배송·세금과
미확인 조건을
함께 표시합니다.

근거: https://github.com/y00nZZang/product-catalog/blob/main/docs/verification.md . 사용자 제공 상품 분석 캡처 원본을 자르지 않고 삽입. 관측·추정값이며 실제 결제액 아님.

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
10/6 확인 소계는 SAZO63,114원, 직접구매+tenso 약64,306원이었습니다.
이 조건에서는 구매대행을 이용하는 편이 유리하다고 느꼈습니다.
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
