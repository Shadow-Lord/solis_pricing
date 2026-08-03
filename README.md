Solis Pricing Engine

A Home Assistant custom integration that calculates daily import and export energy costs for Solis inverters using statistics deltas, tariff windows, and configurable pricing.

This integration is designed for Solis sensors that provide cumulative energy values (with calendar history) and do not reset at midnight.
It computes accurate daily costs by analysing Home Assistant’s statistics history rather than relying on Solis “daily” sensors.

⭐ Features
Accurate daily import cost based on tariff windows

Accurate daily export cost based on fixed export rate

Uses statistics deltas for correct daily kWh

Works with Solis cumulative sensors

Updates automatically every 5 minutes

Exposes two sensors:

sensor.solis_import_cost_today

sensor.solis_export_cost_today

Fully compatible with Casa Luna dashboards

Zero lag — pricing is computed inside Home Assistant, not in the UI

HACS‑friendly structure for easy installation and updates

📦 Installation (HACS)
Option 1 — HACS Custom Repository (recommended)
Open HACS → Integrations

Click the three dots → Custom repositories

Add your repository URL:

Code
https://github.com/<your-user>/solis_pricing
Category: Integration

Click Add

Install Solis Pricing Engine from HACS

Restart Home Assistant

📁 Manual Installation
Copy the folder:

Code
custom_components/solis_pricing/
into:

Code
config/custom_components/solis_pricing/
Restart Home Assistant.

⚙️ Configuration
Add this to your configuration.yaml:

yaml
sensor:
  - platform: solis_pricing
This will create:

sensor.solis_import_cost_today

sensor.solis_export_cost_today
