//------------- tables-data.js -------------//
$(document).ready(function() {

	

	//------------- Data tables -------------//
	//basic datatables
	$('#basic-datatables').dataTable({
		"oLanguage": {
		    "sSearch": "إبحث ",
		    "sLengthMenu": "<span>_MENU_</span>",
		    "sLengthMenu": "عرض _MENU_ لكل صفحة",
			"sZeroRecords": "لم يتم العثور على شيء - آسف",
			"sInfo": "عرض _START_ إلى _END_ من _TOTAL_ تسجيلات",
			"sInfoEmpty": "عرض  0 إلى  0 من  0 تسجيلات",
			"sInfoFiltered": "(تمت تصفيت _MAX_ من إجمالي السجلات)",
			 "oPaginate": {
            "sFirst":    "الأول",
            "sLast":    "الأخير",
            "sNext":    "القادم",
            "sPrevious": "السابق"
        	},
		},
		"sDom": "<'row'<'col-md-6 col-xs-12 'l><'col-md-6 col-xs-12'f>r>t<'row'<'col-md-4 col-xs-12'i><'col-md-8 col-xs-12'p>>"
	});

	//vertical scroll
	$('#vertical-scroll-datatables').dataTable( {
		"scrollY":        "200px",
		"scrollCollapse": true,
		"paging":         false
	});

	//responsive datatables
	$('#responsive-datatables').dataTable({
		"oLanguage": {
		    "sSearch": "إبحث ",
		    "sLengthMenu": "<span>_MENU_</span>",
		    "sLengthMenu": "عرض _MENU_ لكل صفحة",
			"sZeroRecords": "لم يتم العثور على شيء - آسف",
			"sInfo": "عرض _START_ إلى _END_ من _TOTAL_ تسجيلات",
			"sInfoEmpty": "عرض  0 إلى  0 من  0 تسجيلات",
			"sInfoFiltered": "(تمت تصفيت _MAX_ من إجمالي السجلات)",
			 "oPaginate": {
            "sFirst":    "الأول",
            "sLast":    "الأخير",
            "sNext":    "القادم",
            "sPrevious": "السابق"
        	},
		},
		"sDom": "<'row'<'col-md-6 col-xs-12 'l><'col-md-6 col-xs-12'f>r>t<'row'<'col-md-4 col-xs-12'i><'col-md-8 col-xs-12'p>>"
	});

	//with tabletools
	$('#tabletools').DataTable( {
		"oLanguage": {
		    "sSearch": "",
		    "sLengthMenu": "<span>_MENU_</span>"
		},
		"sDom": "T<'row'<'col-md-6 col-xs-12 'l><'col-md-6 col-xs-12'f>r>t<'row'<'col-md-4 col-xs-12'i><'col-md-8 col-xs-12'p>>",
		tableTools: {
			"sSwfPath": "http://cdn.datatables.net/tabletools/2.2.2/swf/copy_csv_xls_pdf.swf",
			"aButtons": [ 
		      "copy", 
		      "csv", 
		      "xls",
		      "print",
		      "select_all", 
		      "select_none" 
		  ]
		}
	});
	
});