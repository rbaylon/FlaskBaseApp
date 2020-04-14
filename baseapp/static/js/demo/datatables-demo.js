// Call the dataTables jQuery plugin
$(document).ready(function() {
  $('#dataTable').DataTable({ "lengthMenu": [ [10, 100, 1000, -1], [10, 100, 1000, "All"] ] });
});
