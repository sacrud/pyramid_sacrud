requirejs.config({
  "paths": {
    "app": "app",

    "jquery": "lib/jquery.min",
    "chosen": "lib/chosen.jquery.min",
    "jquery-ui": "lib/jquery-ui.min",
    "speakingurl": "lib/speakingurl.min",
    "jquery-ui-timepicker-addon": "lib/jquery-ui-timepicker-addon",

    "popup": "app/common/popup",
    "checkbox": "app/common/checkbox",
    "selectable": "app/common/selectable",
  },
  "shim": {
      "jquery.alpha": ["jquery"],
      "jquery.beta": ["jquery"]
  }
})
