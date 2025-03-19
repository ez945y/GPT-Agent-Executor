import asyncio
import websockets
import json

async def websocket_client(uri):
    """
    建立 WebSocket 客戶端並連接到指定的 URI。

    Args:
        uri (str): WebSocket 伺服器的 URI。
    """
    try:
        async with websockets.connect(uri) as websocket:
            print(f"Connected to {uri}")

            # 發送初始訊息 (可選)
            initial_message = {"message": "Hello, WebSocket server!"}
            await websocket.send(json.dumps(initial_message))

            # 接收訊息
            async for message in websocket:
                try:
                    data = json.loads(message)
                    print(f"Received: {data}")

                    # 根據接收到的訊息執行相應的操作
                    if data.get("type") == "updateConversation":
                        print("updateConversation received")
                        #處理updateConversation
                    elif data.get("type") == "error":
                        print("Error received")
                        #處理error
                    elif data.get("type") == "logs_update":
                        print("logs_update received")
                        #處理logs_update

                    # 回應訊息 (可選)
                    response_message = {"response": "Message received!"}
                    await websocket.send(json.dumps(response_message))

                except json.JSONDecodeError:
                    print(f"Received non-JSON message: {message}")

    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Connection closed unexpectedly: {e}")
    except websockets.exceptions.InvalidURI as e:
        print(f"Invalid URI: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    uri = "ws://127.0.0.1:8000/wwss"  # 替換為您的 WebSocket 伺服器 URI
    asyncio.run(websocket_client(uri))