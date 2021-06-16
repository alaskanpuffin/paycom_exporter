# paycom_exporter
Prometheus exporter for Paycom Timeclock Sync Status

Disable 2FA and set all security questions to the same answer.

Default port `9770`

Required Environment Variables
`paycom_code` - Paycom Site Code
`paycom_username` - Paycom Username
`paycom_password` - Paycom Password
`paycom_question` - Paycom Security Question Answer

The results are cached for 15 minutes.