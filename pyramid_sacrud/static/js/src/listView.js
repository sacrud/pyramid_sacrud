import {
  grid_view,
  delete_button,
  select_all_item,
  table_checkboxes,
  table_checkboxes_checked
} from './settings';

$(() => {
  /*
   * Run only on list of rows in table view.
   */
  if($(grid_view).length) {
    selectAllHandler();
    deleteButtonHandler();
  }
});

class DeleteButton {
  /*
   * Delete button disable/enable
   */
  constructor(selector) {
    this.obj = selector;
  }

  get disable() {
    if(this.obj.hasClass("disabled"))
      return true;
    else
      return false;
  }

  set disable(value) {
    if(value===true)
      this.obj.removeClass("red").addClass("disabled");
    else
      this.obj.removeClass("disabled").addClass("red");
  }
}

function selectAllHandler() {
  /*
   * Select all checkboxes handler.
   */

  let $selectAll = $(select_all_item);
  let $items = $(table_checkboxes);

  // add multiple select / deselect functionality
  $selectAll.click(function() {
    $items.prop('checked', this.checked);
  });

  // if all checkbox are selected, check the selectall checkbox
  // and viceversa
  $items.click(() => {
    if($items.length == $(table_checkboxes_checked).length) {
      $selectAll.prop("checked", "checked");
    } else {
      $selectAll.removeAttr("checked");
    }
  });
}

function popupWindow(message) {
  /*
   * Show popup window with message.
   */
  let $deleteConfirmBtn = $("#delete-confirm");
  $deleteConfirmBtn.click(() => {
    $("#mass-action").val("delete");
    $("#sacrud-form").submit();
  });
  $("#modal1").openModal();
}

function deleteButtonHandler() {
  /*
   * Disable/enable delete button handler.
   */
  let $items = $(table_checkboxes);
  let $selectAll = $(select_all_item);
  let $deleteButton = new DeleteButton($(delete_button));
  let handler = () => {
    if($(table_checkboxes_checked).length)
      $deleteButton.disable = false;
    else
      $deleteButton.disable = true;
  };
  handler();
  $items.on('change', handler);
  $selectAll.on('change', handler);

  // Show popup window after click if button enabled.
  $deleteButton.obj.click(() => {
    if(!$deleteButton.disable) {
      popupWindow("");
    }
  });
}


