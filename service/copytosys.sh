#!/bin/bash

# ตรวจสอบว่ามีสิทธิ์ root หรือไม่
if [ "$EUID" -ne 0 ]; then
  echo "กรุณารันสคริปต์นี้ด้วยสิทธิ์ root."
  exit 1
fi

# คัดลอกไฟล์ service ทั้งหมดจากไดเรกทอรีปัจจุบันไปยัง /etc/systemd/system/
for service_file in *.service; 
do
  if [ -f "$service_file" ]; then
    echo "คัดลอก $service_file ไปที่ /etc/systemd/system/"
    cp "$service_file" /etc/systemd/system/
  else
    echo "ไม่พบไฟล์ $service_file ในไดเรกทอรีปัจจุบัน"
  fi
done

# รีโหลด systemd daemon เพื่อให้รู้จักกับการเปลี่ยนแปลง
echo "รีโหลด systemd daemon"
systemctl daemon-reload

echo "เสร็จสิ้นการคัดลอกไฟล์ service"
