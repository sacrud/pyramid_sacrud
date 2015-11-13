import '../../css/materialize.scss'
import 'materialize-js';

$(document).ready(() => {
  $('select').material_select();
  $('.modal-trigger').leanModal();
});
