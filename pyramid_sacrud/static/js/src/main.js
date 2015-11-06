import '../../css/main.scss';
import './materialize';
import {select_all_checkbox, table_checkboxes} from './settings';


$(() => {
  // add multiple select / deselect functionality
  $(select_all_checkbox).click(() => {
    $(table_checkboxes).attr('checked', this.checked);
  });

  // if all checkbox are selected, check the selectall checkbox
  // and viceversa
  $(table_checkboxes).click(() => {
    if($(table_checkboxes).length == $(table_checkboxes + ":checked").length) {
      $(select_all_checkbox).attr("checked", "checked");
    } else {
      $(select_all_checkbox).removeAttr("checked");
    }

  });
});
