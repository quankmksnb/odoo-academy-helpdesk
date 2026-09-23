# =====================================================================
# Script chạy Odoo 19 NATIVE (không dùng Docker)
#
# Cách dùng:
#   .\run-odoo.ps1                        # chạy server bình thường
#   .\run-odoo.ps1 -u academy_helpdesk    # cập nhật (upgrade) module
#   .\run-odoo.ps1 -i academy_helpdesk    # cài (install) module lần đầu
#   .\run-odoo.ps1 -d hoc_odoo -u academy_helpdesk   # chỉ định database
#
# Mọi tham số bạn gõ thêm sẽ được chuyển thẳng cho odoo-bin.
# =====================================================================

$Python  = "D:\iDB\odoo-src\venv\Scripts\python.exe"
$OdooBin = "D:\iDB\odoo-src\odoo-bin"
$Config  = "D:\iDB\project\config\odoo.local.conf"

Write-Host "Khoi dong Odoo 19 (native)..." -ForegroundColor Cyan
Write-Host "Web: http://localhost:8069" -ForegroundColor Green

& $Python $OdooBin -c $Config @args
