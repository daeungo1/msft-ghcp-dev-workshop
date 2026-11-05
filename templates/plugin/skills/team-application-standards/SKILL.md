---
name: team-application-standards
description: "Use when: creating or modernizing a Node.js/TypeScript or Python service that must follow AI MSFT runtime floors, Clean Architecture boundaries, module ownership, and incremental refactoring rules."
---

# AI MSFT Team Application Standards

## 적용 범위

새 애플리케이션, 신규 module/service, legacy module refactoring, runtime
upgrade plan에 이 skill을 적용합니다. 기존 코드 전체를 한 번에 재구성하지
않고 현재 작업이 소유한 module/service boundary부터 적용합니다.

## 1. Runtime lifecycle policy

### Node.js

* Hard floor: `Node.js >=22`
* Node.js 20과 그 이하는 신규 build, CI, production target으로 허용하지 않음
* Production target은 공식 release schedule에서 `Active LTS` 또는
  `Maintenance LTS` 상태인 major만 허용
* `Alpha`와 `Current` release는 evaluation과 CI compatibility testing에만 사용
* 신규 서비스는 조직이 승인한 최신 Active LTS를 기본값으로 선택
* 선택한 release가 12개월 안에 EOL이면 feature implementation 전에 runtime
  upgrade task를 plan에 추가
* `package.json.engines.node`, `.nvmrc` 또는 `.node-version`, Dev Container,
  CI matrix가 같은 major policy를 표현해야 함
* CI는 minimum supported major와 preferred LTS를 함께 검증

```json
{
  "engines": {
    "node": ">=22"
  }
}
```

### Python

* Hard floor: `Python >=3.12`
* 신규 서비스는 조직이 승인한 latest bugfix-supported Python을 우선 선택
* EOL Python을 지원 범위나 CI matrix에 남겨 두지 않음
* `pyproject.toml`의 `requires-python`, Dev Container, CI matrix가 일치해야 함
* Public functions, ports, use cases, DTOs에 type hints를 사용
* Python version을 올릴 때 minimum version과 dependency compatibility를
  동시에 검증하고 lock file을 갱신

```toml
[project]
requires-python = ">=3.12"
```

### Runtime decision record

Plan에 다음을 기록합니다.

1. minimum supported runtime
2. preferred runtime
3. official lifecycle source와 EOL date
4. CI matrix
5. runtime upgrade가 feature delivery보다 먼저 필요한지

## 2. Module-first Clean Architecture

먼저 business capability 기준으로 module/service를 나누고, 각 module 내부에
Clean Architecture dependency rule을 적용합니다. 전역 `controllers/`,
`services/`, `repositories/`, `utils/` 폴더에 모든 domain을 섞지 않습니다.

```text
module/service
├── core
│   ├── entities and value objects
│   └── domain policies
├── application
│   └── use cases
├── ports
│   ├── repositories
│   └── external service contracts
├── adapters
│   ├── inbound HTTP, CLI, messages
│   └── outbound database, queue, external API
└── public API or composition entry point
```

### Dependency direction

```text
Adapters → Application Use Cases → Core
             ↓
            Ports
```

Rules:

* Core는 framework, HTTP, ORM, file system, environment variable을 import하지 않음
* Application Use Cases는 workflow를 orchestration하고 transaction boundary를
  소유하지만 concrete adapter를 import하지 않음
* Ports는 Core 또는 Application이 필요로 하는 interface를 정의
* Adapters는 ports를 구현하고 framework-specific 변환을 담당
* Composition root만 concrete adapter를 use case에 연결
* Cross-module 호출은 상대 module의 public API, port, event contract로만 수행
* ORM entity와 framework request object를 Core로 전달하지 않음

## 3. Python service example

```text
src/app/orders/
├── core/
│   ├── entities.py
│   └── policies.py
├── application/
│   ├── create_order.py
│   └── cancel_order.py
├── ports/
│   ├── order_repository.py
│   └── payment_gateway.py
├── adapters/
│   ├── http/routes.py
│   ├── persistence/sqlalchemy_repository.py
│   └── payments/http_gateway.py
├── api.py
└── wiring.py
```

Python rules:

* `core/`와 `application/`은 SQLAlchemy와 FastAPI를 import하지 않음
* `ports/`는 `Protocol` 또는 abstract base class로 typed contract를 제공
* FastAPI dependency injection과 SQLAlchemy session은 `adapters/`와
  `wiring.py`에 제한
* 다른 module은 `api.py`만 import
* import-linter로 dependency direction과 public boundary를 자동 검증

## 4. Node.js and TypeScript service example

```text
src/modules/orders/
├── core/
│   ├── order.ts
│   └── order-policy.ts
├── application/
│   ├── create-order.ts
│   └── cancel-order.ts
├── ports/
│   ├── order-repository.ts
│   └── payment-gateway.ts
├── adapters/
│   ├── http/order-routes.ts
│   ├── persistence/sql-order-repository.ts
│   └── payments/http-payment-gateway.ts
├── index.ts
└── wiring.ts
```

TypeScript rules:

* `core/`와 `application/`은 Express, NestJS, ORM package를 import하지 않음
* `ports/`는 narrow interface를 정의하고 adapters가 이를 구현
* `any`를 사용하지 않고 boundary input은 schema validation 후 typed DTO로 변환
* 다른 module은 `index.ts`의 exported contract만 import
* dependency-cruiser, ESLint boundary rules 또는 equivalent tool로 dependency
  direction을 검증

## 5. Incremental refactoring pattern

Refactoring unit은 전체 layer가 아니라 **one module/service or one use case**입니다.

1. Characterize: 현재 public behavior를 acceptance 또는 characterization test로 고정
2. Select seam: HTTP route, message handler, scheduled job, public function 중
   하나의 entry point를 선택
3. Define contract: DTO, port, error contract, transaction behavior를 명시
4. Extract Core: framework-independent business rule을 이동
5. Extract Application Use Case: orchestration과 transaction boundary를 이동
6. Wrap infrastructure: 기존 DB/API 호출을 adapter로 감싸 port를 구현
7. Switch one entry point: 선택한 seam만 새 use case로 전환
8. Verify: old/new behavior, contract, architecture boundary, performance를 검증
9. Remove legacy: caller가 0개이고 tests가 green일 때만 이전 path 제거

Legacy modernization에는 Strangler Fig approach를 사용합니다. Facade 또는
router가 legacy와 new module을 함께 지원하고, use case 단위로 traffic을
이동합니다. Big-bang rewrite는 사용자가 명시적으로 요구하고 rollback과
behavior parity evidence가 있을 때만 선택합니다.

## 6. Optional Integration Wrapper Shape

이 구조는 **여러 MCP/API/database를 하나의 catalog로 제공해야 할 때만**
선택합니다. 단일 external system은 해당 module의 port와 adapter로 직접
연결하며 registry를 추가하지 않습니다.

이 skill은 wrapper 구현을 제공하거나 특정 manifest schema를 강제하지
않습니다. 다음 responsibility shape만 참고해 프로젝트 규모와 보안 요구에
맞게 설계합니다.

```text
Application Use Case
        ↓
Integration Port
        ↓
Resource Descriptor
        ↓
Resource Registry
        ↓
Adapter Router
├── HTTP Adapter
├── MCP Adapter
└── Database Adapter
```

Minimal rules:

* Resource descriptor에는 `id`, protocol type, connection environment key,
  operation, input/output contract만 둠
* Registry는 descriptor validation과 duplicate detection만 담당
* HTTP, MCP, Database protocol detail은 각각 adapter에 격리
* URL과 secret은 descriptor에 넣지 않고 environment 또는 secret store에서 주입
* Remote MCP tool은 allowlist로 제한하고 database adapter는 read-only와
  parameter binding을 기본값으로 사용
* Invalid descriptor를 조용히 skip하지 않고 startup 또는 build를 실패시킴

도입 전 확인:

1. External resource가 3개 이상이거나 비개발자도 catalog를 확장해야 하는가?
2. Resource별 input/output contract와 authorization boundary가 필요한가?
3. Registry와 protocol adapter의 운영 비용보다 중복 wrapper 감소 효과가 큰가?

세 질문 중 하나라도 아니면 module-local port와 adapter를 사용합니다.

Shape reference:
https://github.com/hy2219/simplified-sdlc

## 7. Contract and data rules

* HTTP, events, database schema는 explicit contract로 취급
* Core entity를 API response나 ORM entity로 직접 재사용하지 않음
* Inbound adapter가 external input을 DTO로 변환하고 validation
* Outbound adapter가 domain value를 persistence/external format으로 변환
* Idempotency, retries, timeout, transaction scope는 Application Use Case에 명시
* Error는 stable code와 user-safe message를 사용하고 internal exception을 노출하지 않음
* Cross-service integration은 versioned API/event contract와 contract test를 가짐

## 8. Test strategy by layer

| Layer | Test type | External dependency |
|---|---|---|
| Core | fast unit tests and property tests | none |
| Application Use Cases | use-case tests with typed fakes | ports only |
| Adapters | integration tests | real DB, queue, HTTP test server |
| Public contracts | contract tests | serialized requests, events, responses |
| User scenarios | acceptance tests | deployable slice |

Rules:

* Core test에서 framework와 database를 mock하지 않음
* Use case test는 adapter implementation이 아니라 port behavior를 fake
* Adapter integration test는 실제 serialization, query, transaction을 검증
* Acceptance criterion 하나에 observable behavior test 하나를 연결
* Test expectation을 implementation에 맞춰 약화하지 않음

## 9. Architecture automation

Project post-edit 및 CI에 다음 검사를 연결합니다.

* runtime floor and lock-file validation
* type checking
* formatter and lint
* unit, integration, contract, acceptance tests
* module dependency boundary rules
* public API and schema compatibility
* secret and dependency vulnerability scanning

Optional multi-resource shape를 채택한 경우에만 descriptor/registry validation과
protocol adapter contract tests를 추가합니다.

Python은 import-linter, TypeScript는 dependency-cruiser 또는 ESLint boundary
rules를 기본 후보로 사용합니다. 도구가 다르더라도 dependency direction
contract는 동일해야 합니다.

## 10. Reject criteria

다음 변경은 plan 단계에서 거부하거나 다시 분해합니다.

* EOL runtime을 신규 target으로 추가
* 전체 application을 한 번에 Clean Architecture로 이동
* Core에서 ORM, HTTP framework, environment variable 직접 접근
* module이 다른 module의 repository 또는 internal service를 직접 import
* DTO 없이 external payload를 business rule에 전달
* one task에서 여러 service의 migration과 behavior change를 동시에 수행
* architecture boundary test 없이 directory만 재배치
* old path caller가 남아 있는데 legacy code 제거
Optional multi-resource shape를 채택한 경우 다음도 거부합니다.

* external API URL, token, password를 resource descriptor에 저장
* descriptor validation 없이 MCP/API tool을 자동 노출
* database adapter가 arbitrary SQL 또는 write operation을 허용

## 11. Completion evidence

완료 보고에는 다음을 포함합니다.

1. 선택한 runtime versions와 lifecycle 근거
2. refactoring 대상 module/service와 selected seam
3. Core, Application Use Cases, Ports, Adapters 변경 파일
4. dependency boundary 검사 결과
5. layer별 test 명령과 통과 수
6. legacy path caller count 또는 남은 migration task
7. Optional multi-resource shape를 채택한 경우에만 descriptors, registry,
   adapter contract test 결과

## Official references

* Node.js supported production releases:
  https://nodejs.org/en/about/previous-releases
* Node.js release schedule: https://github.com/nodejs/Release
* Python version status: https://devguide.python.org/versions/
* Microsoft architectural principles:
  https://learn.microsoft.com/dotnet/architecture/modern-web-apps-azure/architectural-principles
* Microsoft Clean Architecture guidance:
  https://learn.microsoft.com/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures
* Azure Strangler Fig pattern:
  https://learn.microsoft.com/azure/architecture/patterns/strangler-fig
* Shape reference for a manifest-driven MCP resource catalog:
  https://github.com/hy2219/simplified-sdlc
