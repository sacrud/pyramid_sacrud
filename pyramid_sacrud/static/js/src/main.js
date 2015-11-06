import '../../css/main.scss';
import './materialize';
import select_all_checkbox from './settings';

$(select_all_checkbox).change(() => {
  $("input:checkbox").prop('checked', $(this).prop("checked"));
});
