# 로컬 도구 계약 (v0.1)

모든 명령은 `python3 <plugin-root>/scripts/purchase_agent.py ...`. root는 이 문서의 상위 디렉터리다. 인수 JSON은 비공개 파일을 사용하고 셸 명령에 개인정보를 직접 쓰지 않는다. 외부 사이트를 호출하는 명령은 없다. 기본 state-dir은 저장소 밖이며 테스트는 임시 디렉터리로 격리한다.

## 의도·승인·시도

`create <intent.json>` → run ID, intent_digest. 같은 조건의 활성 실행이 있으면 기존 run을 반환한다. `status RUN`은 식별자 원문을 제외한 요약, `inspect RUN`은 비공개 전체 내역이다. 중복 감지는 같은 정규화 상품 URL/옵션/수령 별칭에 의존하므로 에이전트가 별칭·URL이 다른 기존 주문도 대조해야 한다.

Intent 필수 필드(예시 값은 합성):
```json
{
  "product_url": "https://books.rakuten.co.jp/rb/12345678/",
  "product_key": "sample-model-A",
  "title": "Sample product",
  "seller": "Rakuten Books",
  "quantity": 1,
  "options": {},
  "condition": "new",
  "currency": "JPY",
  "total": "5000",
  "destination": "KR",
  "forwarder": "malltail",
  "center": "JP",
  "recipient_ref": "saved-profile-A"
}
```
`total`은 판매점 주문 결제 합계이며 국제배송비와 분리한다. 특정 판본/색상 등은 options 또는 product_key로 정확히 구별한다. 수정할 필요가 생기면 외부 주문 부재를 확인 후 기존 실행을 근거와 함께 cancel하고 새 의도로 만든다.

사람이 실제 확인한 뒤 `approve RUN <approval.json>`:
```json
{
  "intent_digest": "create/status 결과의 digest",
  "max_total": "5000",
  "expires_at": "실제 사용자 승인의 ISO8601 시각(+09:00 등 시간대 포함)",
  "user_evidence_ref": "해당 사용자 승인 메시지 참조",
  "allow_forwarding": true,
  "allow_tracking_update": false
}
```
만료는 구매 시도에 적용한다. 배송신청/운송장 보완 권한은 해당 주문의 후속 처리 범위다. 가격·주소·새 비용·조건 변경은 기존 권한으로 추론하지 않는다. 이 기록은 사용자 승인 진위를 독립 검증하지 못하며 skill이 실제 메시지를 확인한다.

`begin RUN purchase --input <fresh-checkout.json>`: 같은 intent 구조. 모든 비가격 필드 동일, total은 승인 상한 이하, 유효기간·지원 경로 충족이어야 성공. 성공하면 pending attempt ID가 생긴다. 이 명령이 외부 주문을 만들지는 않는다. 그 후 현재 도구의 승인 규칙을 따라 주문을 한 번 수행한다.

`begin RUN forwarding` / `begin RUN tracking_update`: 확인된 주문/신청과 허용 범위 필요. `resolve RUN <result.json>`:
```json
{
  "attempt_id": "begin이 반환한 pending_action.id",
  "outcome": "confirmed",
  "evidence_ref": "실제 주문/신청 내역의 비공개 참조",
  "external_ref": "실제 주문번호 또는 신청번호 또는 운송장"
}
```
`outcome`은 confirmed / not_applied / unknown. unknown은 pending을 유지한다. not_applied는 외부 상태 조회로 작업이 적용되지 않았음을 확인한 경우에만 사용하며 누락 메일 하나로 판단하지 않는다. begin 후 프로세스가 죽어도 다른 실행은 pending에서 멈춘다. SQLite 트랜잭션이 같은 state DB의 경합을 직렬화한다. 다른 DB를 쓰면 이 보호를 공유하지 못한다.

## 추적 사건

`observe RUN <event.json>`:
```json
{
  "id": "안정적인 원본 사건 참조",
  "stage": "seller_shipped",
  "order_ref": "이 run의 실제 주문번호",
  "evidence_ref": "발송 메일 또는 사이트 상태의 비공개 참조",
  "occurred_at": "2026-10-05T10:00:00+09:00",
  "observed_at": "2026-10-05T11:00:00+09:00"
}
```
실제 관측시각을 사용한다. stage 허용값은 tracking.md 참조. id 중복은 무시하고 과거 단계로 회귀하지 않는다. 배송완료는 delivered이며 사용자 확인 received에서 run을 닫는다. `cancel RUN <json>`은 `{ "evidence_ref": "취소 근거 참조" }`. 외부 취소를 수행하지 않는다. pending이 있으면 먼저 reconcile한다.

`schedule-plan RUN`은 반복 프롬프트 제안만 출력한다. 공식 도구에서 실제 등록 성공 후 `attach-schedule RUN <json>`에 `{ "automation_ref": "도구가 반환한 ID" }`를 넣는다. 이미 다른 ID가 있으면 중복 생성을 막는다. 실제 변경/종료는 예약 도구에서 수행한다.

## 견적 JSON

`quote <quotes.json>`은 아래 구조. context 객체를 각 행에도 동일하게 기록해 서로 다른 조건 섞임을 탐지한다. 소수 금액은 문자열로 입력한다. quote.components는 아래 6개 키를 모두 갖고, 미확인은 null이다.
```json
{
  "context": {
    "product_key": "sample-model-A", "quantity": 1, "destination": "KR",
    "package": {"weight_g": "250", "dimensions_cm": ["19", "14", "2"], "basis": "assumed"}
  },
  "quotes": [{
    "provider": "sample-forwarder", "method": "EMS", "status": "available",
    "context": {
      "product_key": "sample-model-A", "quantity": 1, "destination": "KR",
      "package": {"weight_g": "250", "dimensions_cm": ["19", "14", "2"], "basis": "assumed"}
    },
    "source_url": "https://example.com/fees", "observed_at": "2026-10-05T10:00:00+09:00", "expires_at": "2026-10-05T11:00:00+09:00",
    "components": {
      "goods": {"amount": "5000", "currency": "JPY", "basis": "quoted"},
      "domestic_shipping": {"amount": "0", "currency": "JPY", "basis": "confirmed_zero"},
      "handling": null, "international_shipping": null, "mandatory_options": null, "tax": null
    },
    "tracking": "unverified", "compensation": "unverified", "benefits": "none"
  }]
}
```
위 수치는 실행용 최신 견적이 아니다. 무게가 불명확하면 package basis=unknown, weight_g/dimensions_cm=null. KRW 비용이 있으면 최상위 fx 필수: krw_per_100_jpy, source_url, basis_date, observed_at, expires_at, kind. 예: 종류 mid-market, 단위는 필드명에 고정. 한 quote에 서로 다른 통화의 비용을 넣어도 항목별로 환산하고 합계에서만 반올림한다. USD 등 다른 통화는 v0.1 계산기 미지원으로 명시하며 탐색을 막지는 않는다.

## HTML 후보 추출

`extract <public-html-file> --url <public-product-url>`은 네트워크 없이 JSON-LD Product 후보만 추출한다. 복수 후보·옵션을 자동 선택하지 않는다. visible DOM만 있는 페이지는 브라우저로 읽어 같은 관측 필드를 작성한다. JSON-LD 부재가 상품 부재를 의미하지 않는다.

## 조회 성공/실패 기록

`record-check RUN <json>`: `{ "success": true, "observed_at": "시간대 포함 현재 시각", "evidence_ref": "조회 근거 참조" }`. 실패 때 false로 기록하며 last_success_at을 보존한다. `status`의 last_check_at/last_success_at을 이용해 미조회 기간을 설명한다. 개인정보가 들어간 에러 원문은 저장하지 않는다.
