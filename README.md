# Arduino-Pulse-Sensor-Python-GUI

Bu proje, bir Arduino Uno kullanarak nabız sensöründen veri ölçmeyi ve Python Tkinter tabanlı bir arayüz ile sonuçları görüntülemeyi amaçlar. Kullanıcıların gerçek zamanlı olarak nabızlarını izlemelerini sağlayan bir uygulama oluşturulmuştur.

## Bileşenler
- Arduino Uno: Sensör verilerini işleyen mikrodenetleyici.
- Nabız Sensörü: KY-039
- Python: Grafiksel kullanıcı arayüzü için kullanılan programlama dili.
- Tkinter: Python kütüphanesi, GUI oluşturmak için kullanılır.

## Kurulum
Nabız sensörünü Arduino Uno'ya bağlayın. Genellikle bu bağlantılar şu şekildedir:
1. VCC'yi 5V pinine bağlayın.
2. GND'yi GND pinine bağlayın.
3. Signal pinini bir analog giriş pinine (örneğin, A0) bağlayın.
4. Arduino Kodunu Yükleyin
5. Arduino IDE kullanarak sağlanan kodu Arduino Uno'ya yükleyin. Kod, nabız sensöründen veri okur ve bilgisayara seri iletişim yoluyla gönderir.
## Kullanım
- Uygulamayı Başlatın: Python betiğini çalıştırarak GUI'yi başlatın.
- Arduino'yu Bağlayın: Arduino Uno'nun bilgisayara USB ile  COM4 'e bağlı olduğundan emin olun.
- Nabızı İzleyin: GUI, gerçek zamanlı nabız verilerini gösterecektir.
- Form uygulamasını kullanarak, bir kullanıcı kaydı oluşturabilirsiniz. Giriş yaptıktan sonra 30 saniye boyunca nabız sensörüne parmağınızı yerleştirin ve nabız değerlerinizi takip edin. Eski nabız değerlerinizi grafik üzerinde gözlemleyebilir ve takip edebilirsiniz.

## Video
Projenin çalışır halini aşağıdan izleyebilirsiniz.

https://github.com/user-attachments/assets/c2e62308-ca47-4138-869b-cc21c47b5000

