window.DASH = {
 "headline": {
  "requests": 202650,
  "success": 192854,
  "cost": 5711.2498,
  "kwh": [
   276.6037,
   386.4908,
   496.3779
  ],
  "kgco2e": [
   26.000799999999998,
   135.2717,
   291.8701
  ]
 },
 "cards": [
  {
   "tenant": "org-engineering-dev",
   "persona": "Engineering / Developers",
   "provider": "openai",
   "outlier": true,
   "requests": 33291,
   "prompt_median": 8038.0,
   "cache_pct": 2.7039,
   "r400_pct": 6.1174,
   "premium_pct": 68.7423,
   "cost_per": 0.0554,
   "wh_per": 2.2893
  },
  {
   "tenant": "org-marketing-ai",
   "persona": "Marketing / Communications",
   "provider": "openai",
   "outlier": false,
   "requests": 35074,
   "prompt_median": 4315.5,
   "cache_pct": 22.4204,
   "r400_pct": 1.1123,
   "premium_pct": 53.2759,
   "cost_per": 0.0383,
   "wh_per": 1.9388
  },
  {
   "tenant": "org-prod-core",
   "persona": "Core Production Services",
   "provider": "openai",
   "outlier": false,
   "requests": 34846,
   "prompt_median": 4252.0,
   "cache_pct": 22.6263,
   "r400_pct": 1.2421,
   "premium_pct": 52.6603,
   "cost_per": 0.0364,
   "wh_per": 1.8978
  },
  {
   "tenant": "prj-ai-enterprise-prod",
   "persona": "Enterprise Production",
   "provider": "gemini",
   "outlier": false,
   "requests": 30274,
   "prompt_median": 3692.5,
   "cache_pct": 18.7959,
   "r400_pct": 1.1611,
   "premium_pct": 47.374,
   "cost_per": 0.0106,
   "wh_per": 1.6919
  },
  {
   "tenant": "prj-ai-r-and-d",
   "persona": "Researchers (R&D)",
   "provider": "gemini",
   "outlier": false,
   "requests": 30485,
   "prompt_median": 3692.0,
   "cache_pct": 19.364,
   "r400_pct": 1.1148,
   "premium_pct": 47.5578,
   "cost_per": 0.0106,
   "wh_per": 1.6939
  },
  {
   "tenant": "prj-ai-sandbox-testing",
   "persona": "Sandbox Testers",
   "provider": "gemini",
   "outlier": true,
   "requests": 28884,
   "prompt_median": 13985.5,
   "cache_pct": 2.4357,
   "r400_pct": 6.0256,
   "premium_pct": 64.7867,
   "cost_per": 0.0212,
   "wh_per": 2.5373
  }
 ],
 "majority": {
  "cache_pct": [
   18.7959,
   22.6263
  ],
  "r400_pct": [
   1.1123,
   1.2421
  ],
  "prompt_median_openai": 4283.75,
  "prompt_median_gemini": 3692.25
 },
 "purpose_share": {
  "Reasoning": {
   "requests": 9.97,
   "cost": 65.05,
   "energy": 32.29
  },
  "Frontier": {
   "requests": 48.09,
   "cost": 34.03,
   "energy": 42.01
  },
  "Small/fast": {
   "requests": 41.94,
   "cost": 0.92,
   "energy": 25.7
  }
 },
 "cost_ratio_reasoning_vs_frontier": 9.226415051439862,
 "opportunity": {
  "org-engineering-dev": {
   "actual_cost": 1843.4715,
   "actual_kwh": 76.2129,
   "levers": [
    {
     "key": "L1_cache",
     "label": "Reuse stable prompt text (cache)",
     "d_cost": -110.0284,
     "d_cost_pct": -5.9685,
     "d_kwh": -3.2403,
     "d_kwh_pct": -4.2517
    },
    {
     "key": "L2_prompt",
     "label": "Trim prompts",
     "d_cost": -393.0387,
     "d_cost_pct": -21.3206,
     "d_kwh": -8.4765,
     "d_kwh_pct": -11.1221
    },
    {
     "key": "L3_model_mix",
     "label": "Use the small model for routine work",
     "d_cost": -159.3708,
     "d_cost_pct": -8.6451,
     "d_kwh": -1.3765,
     "d_kwh_pct": -1.8061
    },
    {
     "key": "L_all",
     "label": "All three together",
     "d_cost": -572.1273,
     "d_cost_pct": -31.0353,
     "d_kwh": -10.1464,
     "d_kwh_pct": -13.3132
    }
   ],
   "failed_avoided": 1814
  },
  "prj-ai-sandbox-testing": {
   "actual_cost": 613.2647,
   "actual_kwh": 73.2864,
   "levers": [
    {
     "key": "L1_cache",
     "label": "Reuse stable prompt text (cache)",
     "d_cost": -68.4438,
     "d_cost_pct": -11.1606,
     "d_kwh": -5.203,
     "d_kwh_pct": -7.0996
    },
    {
     "key": "L2_prompt",
     "label": "Trim prompts",
     "d_cost": -160.4118,
     "d_cost_pct": -26.157,
     "d_kwh": -13.4563,
     "d_kwh_pct": -18.3612
    },
    {
     "key": "L3_model_mix",
     "label": "Use the small model for routine work",
     "d_cost": -139.6559,
     "d_cost_pct": -22.7725,
     "d_kwh": -3.755,
     "d_kwh_pct": -5.1238
    },
    {
     "key": "L_all",
     "label": "All three together",
     "d_cost": -292.3786,
     "d_cost_pct": -47.6758,
     "d_kwh": -17.1665,
     "d_kwh_pct": -23.4239
    }
   ],
   "failed_avoided": 1541
  }
 },
 "campus_local": {
  "d_cost": -864.5059,
  "d_cost_pct": -15.1369,
  "d_kwh": -27.3129,
  "d_kwh_pct": -7.0669,
  "d_kwh_low": -21.083799999999997,
  "d_kwh_high": -33.542100000000005,
  "failed_avoided": 3355
 },
 "per_purpose": {
  "Reasoning": {
   "cost": 0.28172140252795336,
   "wh": 6.603949829215076
  },
  "Frontier": {
   "cost": 0.03053422168385849,
   "wh": 1.780299135421454
  },
  "Small/fast": {
   "cost": 0.0009479969854469544,
   "wh": 1.2487086244937318
  }
 },
 "kit": {
  "o1-preview": {
   "purpose": "Reasoning",
   "price_in": 15.0,
   "price_cached": 7.5,
   "price_out": 60.0,
   "price_status": "UNVERIFIED-third-party",
   "energy": {
    "a": 1.53508547008547,
    "b_in": 0.00010329914529914533,
    "b_out": 0.0024086153846153845
   },
   "energy_proxy": true,
   "baseline": {
    "prompt": 8023.0,
    "output": 2495.0,
    "cache_share": 0.2462848911706956,
    "hidden_share": 0.5940312648034107
   },
   "outlier": {
    "prompt": 12414.0,
    "output": 2497.5,
    "cache_share": 0.030498355097308406
   }
  },
  "gpt-4o": {
   "purpose": "Frontier",
   "price_in": 2.5,
   "price_cached": 1.25,
   "price_out": 10.0,
   "price_status": "verified-official",
   "energy": {
    "a": 0.12098290598290595,
    "b_in": 0.00013094017094017092,
    "b_out": 0.0009630769230769232
   },
   "energy_proxy": false,
   "baseline": {
    "prompt": 6016.0,
    "output": 1295.0,
    "cache_share": 0.19485891212140102,
    "hidden_share": 0.0
   },
   "outlier": {
    "prompt": 9417.0,
    "output": 1305.0,
    "cache_share": 0.026202983616836262
   }
  },
  "gemini-1.5-pro": {
   "purpose": "Frontier",
   "price_in": 1.25,
   "price_cached": 0.3125,
   "price_out": 5.0,
   "price_status": "UNVERIFIED-third-party",
   "energy": {
    "a": 0.12098290598290595,
    "b_in": 0.00013094017094017092,
    "b_out": 0.0009630769230769232
   },
   "energy_proxy": true,
   "baseline": {
    "prompt": 12011.0,
    "output": 1800.0,
    "cache_share": 0.18442009230163156,
    "hidden_share": 0.0
   },
   "outlier": {
    "prompt": 18764.0,
    "output": 1798.0,
    "cache_share": 0.024528010583018924
   }
  },
  "gpt-4o-mini": {
   "purpose": "Small/fast",
   "price_in": 0.15,
   "price_cached": 0.075,
   "price_out": 0.6,
   "price_status": "verified-official",
   "energy": {
    "a": 0.020111111111111003,
    "b_in": 3.088888888888885e-05,
    "b_out": 0.0018460000000000002
   },
   "energy_proxy": false,
   "baseline": {
    "prompt": 3004.0,
    "output": 804.0,
    "cache_share": 0.2688471362441841,
    "hidden_share": 0.0
   },
   "outlier": {
    "prompt": 4684.5,
    "output": 800.0,
    "cache_share": 0.027275459790160304
   }
  },
  "gemini-1.5-flash": {
   "purpose": "Small/fast",
   "price_in": 0.075,
   "price_cached": 0.01875,
   "price_out": 0.3,
   "price_status": "partly-verified",
   "energy": {
    "a": 0.020111111111111003,
    "b_in": 3.088888888888885e-05,
    "b_out": 0.0018460000000000002
   },
   "energy_proxy": true,
   "baseline": {
    "prompt": 2499.0,
    "output": 599.0,
    "cache_share": 0.21862353763254685,
    "hidden_share": 0.0
   },
   "outlier": {
    "prompt": 3935.0,
    "output": 598.0,
    "cache_share": 0.0228440828026223
   }
  }
 },
 "energy_params": {
  "low_scale": 0.5674,
  "cached_low": 0.0,
  "cached_high": 0.5
 },
 "equivalents": {
  "phone_charge_kwh": 0.019,
  "phone_source": "US EPA Greenhouse Gas Equivalencies Calculator, calculations and references (smartphone charged = 0.019 kWh; DOE/Dommu 2024)",
  "led_bulb_w": 10,
  "led_note": "ASSUMPTION: a typical 10 W LED bulb"
 }
};
