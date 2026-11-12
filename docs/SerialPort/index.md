# SerialPort Android SDK

SerialPort 提供 Android 设备串口访问能力，供 QYTech 硬件驱动与设备控制模块使用。

## 添加依赖

```kotlin
implementation("io.github.qytech:serialport:0.0.5")
```

- 兼容要求：`minSdk = 31`、Java 17。

## 使用方法

在服务层或后台 I/O 线程打开串口并读写数据，销毁前务必调用 `release()` 关闭底层文件描述符与流：

```kotlin
import com.qytech.serialport.SerialPort

val port = SerialPort(
    serial = "/dev/ttyS3",
    baudRate = 115200,
)

// 在后台线程收发字节帧或挂起分片组包（write / read / readAvailable / readPacket）
port.write(commandBytes)
val packet = port.readPacket(waitMs = 30, delayMs = 5)

// 服务退出或切口时释放串口句柄
port.release()
```

- 避免在主线程直接调用阻塞读写接口（`read()`、`readAvailable()`、`write()`）。

## 更新日志

### v0.0.5（2026-08-19）

- 建立 SerialPort 独立发布文档入口。
