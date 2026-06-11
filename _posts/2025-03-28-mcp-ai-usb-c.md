---
layout: post
title: MCP(Model Context Protocol) AI 세상의 USB-C가 등장했다
date: 2025-03-28 15:14:07 +0900
slug: mcp-ai-usb-c
render_with_liquid: false
categories:
- 프로그래밍
- 이모저모
tags: []
last_modified_at: 2025-03-28 15:32:10 +0900
imported_images:
- assets/img/tistory/39/image-001.jpg
- assets/img/tistory/39/image-002.png
- assets/img/tistory/39/image-003.png
source:
  provider: tistory
  id: 39
---

최근 AI 업계에서는 **MCP(Model Context Protocol)**이 화두로 떠오르고 있다. 많은 이들이 MCP를 “AI의 USB-C”에 비유하는 데에는 그만한 이유가 있다. 지금까지는 AI 모델과 외부 도구 또는 데이터 소스를 연결하려면, 모델마다 다른 통합 방식과 API 호출 방식을 따로 구현해야 했기 때문이다.

## NxM 문제: 모델과 도구의 복잡한 연결 구조

예를 들어, 어떤 애플리케이션에서 GPT-4를 이용해 피자를 주문하는 기능을 만든다고 가정해보자. 이 경우, 사용하는 모델이 OpenAI GPT-4인지, Anthropic Claude인지에 따라 함수 호출 방식과 문서가 달라진다. 도구 역시 공급사마다 API 포맷과 응답 형식이 다르다. 이로 인해 개발자는 **N개의 LLM과 M개의 도구** 조합마다 통합 작업을 반복해야 하는 **NxM 문제**에 직면하게 된다.

또한 실시간 정보를 다뤄야 할 때, 모델은 외부 데이터를 직접 불러올 수 없기 때문에 사용자가 중간에서 데이터를 가져와 모델에 전달하고, 다시 그 응답을 받아 다른 시스템에 적용해야 하는 불편한 흐름이 반복된다. 이는 LLM의 활용도를 제한하는 요인으로 작용해왔다.

MCP는 AI 안전성과 상호운용성에 집중해온 Anthropic이 설계한 프로토콜이다. Anthropic은 자사 LLM인 Claude에서 MCP를 먼저 적용하며 프로토콜의 구조를 정립했고, 이를 바탕으로 생태계를 확장하고 있다.

대표적인 사례로, AI 개발 에디터인 Cursor가 MCP를 지원하고 있다. Cursor는 Claude 모델이 외부 도구를 MCP 방식으로 호출하도록 설계되어 있으며, 코드 생성, 테스트 실행, 디버깅까지 모두 하나의 통합 워크플로우 내에서 처리할 수 있게 한다. 이처럼 MCP는 단순한 챗봇을 넘어 실제 개발 환경에서 AI가 도구를 직접 다루는 기반 기술로 진화 중이다.

![](/assets/img/tistory/39/image-001.jpg)

## MPC 표준 프로토콜 JSON-RPC

MCP는 JSON-RPC 2.0 기반의 통신 프로토콜로, LLM이 외부 시스템과 안전하고 일관된 방식으로 상호작용할 수 있도록 설계되었다. 즉, 다양한 AI 모델과 툴 간의 연결을 하나의 통일된 규약으로 관리할 수 있게 해준다.

MCP의 가장 큰 장점은 모델과 툴 사이의 연결 방식이 표준화된다는 것이다. AI 모델은 MCP 형식에 따라 외부 도구를 호출하고 결과를 받을 수 있으며, 툴 구현자는 표준 포맷에 맞춰 인터페이스를 제공하면 된다. 이로 인해 복잡했던 통합 작업이 크게 단순화된다.

## 기존 API 방식 vs MCP 방식

MCP를 이해하려면 기존 함수 호출 방식과 어떻게 다른지를 비교해보는 것이 좋다.

### 기존 API 방식의 흐름

1. 모델이 텍스트 형태로 함수 호출 지시를 생성
   (예: OpenAI의 `function_call` 객체)
2. 애플리케이션이 해당 함수를 호출하여 데이터를 가져옴
3. 결과를 새로운 메시지로 다시 모델에게 전달
4. 모델이 최종 응답을 생성

이 방식은 개발자가 함수 호출부터 결과 전달까지 모든 오케스트레이션을 직접 처리해야 한다. 또한 모델마다 호출 포맷이 달라서 여러 벤더를 동시에 지원하려면 별도의 변환 작업이 필요하다.

### MCP 방식의 흐름

1. 모델이 표준화된 JSON-RPC 호출 메시지를 생성
2. MCP 서버가 지정된 도구를 실행하고 결과를 반환
3. 애플리케이션은 이 결과를 모델에게 전달
4. 모델은 필요시 추가 호출을 수행하고, 최종 응답을 생성

```python
{ 
	"jsonrpc": "2.0", 
    "method": "tools/call", 
    "params": { 
    	"name": "get_current_stock_price", 
        "arguments": { 
        	"symbol": "AAPL", 
            "currency": "USD" 
        } 
    } 
}
```

MCP의 핵심은 모델이 다단계 호출을 주도적으로 처리할 수 있다는 점이다. 툴 호출을 한 번만 하는 것이 아니라, 이전 호출의 결과를 바탕으로 여러 차례 호출을 이어가는 것도 가능하다.

![](/assets/img/tistory/39/image-002.png)

Azure OpenAI의 MCP 프리뷰에서는 한 번의 응답에 여러 개의 툴 호출을 병렬로 포함하는 것도 가능하다. 응답 JSON에는 `tool_calls` 배열로 다수의 호출이 포함되며, 결과는 각각 `tool_call_id`로 연결된다.

또한 MCP는 `tools/list`, `tools/status`, 스트리밍 응답 등 더 풍부한 상호작용을 처리할 수 있어, 복잡한 워크플로우 구현에 적합하다. 다음 게시글에서 자세한 내용을 다루어 보겠다.

## MCP의 가치: 단순한 호출 그 이상

MCP는 단순히 호출 방식을 바꾸는 것이 아니라, AI 모델의 역할 자체를 확장하는 데에 목적이 있다. LLM을 단순한 텍스트 생성기가 아닌, 외부 도구와 상호작용하는 에이전트로 발전시키는 기반이 된다.

- 확장성: MCP를 지원하는 새로운 도구나 모델이 등장해도 동일한 방식으로 통합 가능
- 워크플로우 자동화: 모델 중심의 복합적인 도구 사용 흐름 구성 가능

LangChain이나 Semantic Kernel 같은 프레임워크도 이러한 흐름을 반영하여 MCP 지원을 강화하고 있다. 다만 장기적으로는 이런 프레임워크 없이도 MCP 기반의 기본 구조만으로 다양한 모델과 툴이 자연스럽게 연결되는 생태계가 구축될 수 있다.

## 마치며

MCP는 AI 모델을 “고립된 채팅 시스템”에서 벗어나, 외부 도구와 자유롭게 상호작용하는 맥락 기반 시스템으로 진화시키는 핵심 기술이다. USB-C가 모든 디바이스 간 연결을 표준화했듯이, MCP는 다양한 AI 모델과 툴 간의 연결을 하나의 규약으로 단순화한다.

Anthropic은 Claude를 통해 이 비전을 먼저 실현하고 있으며, Cursor 같은 실제 개발 도구에서도 MCP를 기반으로 한 도구 활용 흐름이 현실화되고 있다.

AI 생태계가 점점 복잡해지고, 다양한 툴과 데이터를 함께 활용하는 방향으로 발전하는 지금, MCP를 잘쓰는 사람이 AI생태계의 승자가 되는것은 아닐까?

![](/assets/img/tistory/39/image-003.png)

gpt로 생성한 마무리 4컷만화~

## References

- [Model Context Protocol (MCP): Integrating Azure OpenAI for Enhanced Tool Integration and Prompting – Microsoft Community Hub](https://techcommunity.microsoft.com/t5/ai-azure-ai-services-blog/model-context-protocol-mcp-integrating-azure-openai-for/ba-p/4057741)
- [What is Model Context Protocol (MCP): Explained in detail – DEV Community](https://dev.to/aws-builders/what-is-model-context-protocol-mcp-explained-in-detail-38ae)
- [Function Calling vs. Model Context Protocol (MCP): What You Need to Know – DEV Community](https://dev.to/nathanlhelms/function-calling-vs-model-context-protocol-mcp-what-you-need-to-know-1g6j)
- [Model Context Protocol explained as simply as possible – Sean Goedecke](https://seangoedecke.com/posts/model-context-protocol-explained/)
- [Anthropic’s Model Context Protocol (MCP): A Deep Dive for Developers – Medium (Amanatullah)](https://medium.com/@amanatullah/anthropics-model-context-protocol-mcp-a-deep-dive-for-developers-c0ea38014899)
- [Model Context Protocol 공식 문서 – Anthropic](https://docs.anthropic.com/en/docs/agents-and-tools/mcp)
- [Model Context Protocol 소개 페이지 – modelcontextprotocol.io](https://modelcontextprotocol.io/introduction)
- [Cursor 공식 사이트 (Claude 기반 코드 에디터)](https://www.cursor.sh/)
