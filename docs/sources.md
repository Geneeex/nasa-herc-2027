# Sources

We use the handbook for competition requirements and manufacturer documentation for component interfaces. Listed component capability still needs to match the exact delivered revision.

| Source | Used for |
| --- | --- |
| [NASA 2027 HERC Handbook](https://www.nasa.gov/wp-content/uploads/2026/08/2027-herc-handbook-layout-aug6-508-1.pdf) | RC Section 6.4, mass scoring Section 8.2 and tasks on printed pages 40-42 (PDF pages 46-48) |
| [Kemo M148A](https://www.kemo-electronic.de/en/Car/Modules/M148A-Battery-guard-12-V-DC.php) | Negative-line switching and pack cutoff |
| [52Pi EP-0225](https://wiki-md.52pi.com/docs/EP-0225) | DC input, one-input restriction and 5.15 V / 5 A USB-PD output |
| [Raspberry Pi hardware](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html) | Pi 5 power, USB loading and RTC |
| [Picamera2 manual](https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf) | Fresh capture, autofocus and capture metadata |
| [TF03 communication reference](https://wiki.dfrobot.com/sen0328/docs/21565) | 3.3 V UART, 115200 baud, frame format and invalid values |
| [SN74AHCT125](https://www.ti.com/product/SN74AHCT125) | 5 V buffer supply and control-signal interface |
| [FS90 positional servo](https://www.pololu.com/product/2818) | Positional servo and 3.3 V control input |
| [Dire Wolf](https://github.com/wb2osz/direwolf) | AX.25/APRS decoding software |
| [FlySky FS-iA10B](https://www.flysky-cn.com/ia10b-canshu) | Receiver supply and interface |
| [Pololu motor-noise guidance](https://www.pololu.com/docs/0J15/9) | Motor suppression and wiring layout |

We do not treat retailer headline current ratings as a substitute for motor/ESC acceptance tests. We do not infer an RC range tolerance from the handbook's HP allowance. Procurement documents are archived separately in [source documents](source-documents/README.md).
