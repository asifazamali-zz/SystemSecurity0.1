    function readTextFile(file,file_path,can_write)
{
	var rawFile = new XMLHttpRequest();
	rawFile.open("GET", file, false);
	rawFile.onreadystatechange = function ()
{
	if(rawFile.readyState === 4)
	{
	if(rawFile.status === 200 || rawFile.status == 0)
	{
		var allText = rawFile.responseText;

		document.getElementById('id_message').style.visibility= 'visible';
		document.getElementById('id_filePath').value=file_path;
		document.getElementById("id_message").innerHTML=allText;
		if(can_write=='True')
			document.getElementById('submit').style.visibility='visible';
	}
	}
}
rawFile.send(null);
}



    function edit_doc(i,list){

        var doc_dropdown = document.getElementsByClassName('privacy_doc');

        while (i--)
            doc_dropdown[0].className='privacy_show';
//            if(list[i]!='0'){
//                doc_dropdown[i][0].defaultSelected=false;
//                doc_dropdown[i][parseInt(list[i])].defaultSelected=true;
//            }

        var s = document.createElement("input");
        var edit = document.getElementById('edit_doc');
        var panel = document.getElementById('doc_panel');
        //doc.style.visibility='visible';
        s.setAttribute('type',"submit");
        s.setAttribute('value',"Save");

        panel.appendChild(s);
        edit.parentNode.removeChild(edit);


    }


	function edit_friend(f_p){
        var doc=document.getElementById('privacy_friend');
        var s = document.createElement("input"); //input element, Submit button
        var edit = document.getElementById('edit_friend');
        edit.parentNode.removeChild(edit);
        doc.style.visibility='visible';
        s.setAttribute('type',"submit");
        s.setAttribute('value',"Save");

        doc.parentNode.appendChild(s);
        if(f_p){
            if(f_p!='0'){
                doc[0].defaultSelected=false;
                doc[parseInt(f_p)].defaultSelected=true;
            }
        }
    }

    function edit(n,a,l,p,e,name,age,location,phnumber,email){




        var name=document.getElementById("name");
        var age=document.getElementById("age");
        var location=document.getElementById("location");
        var phnumber=document.getElementById("phnumber");
        var email=document.getElementById("email");



        var edit = document.getElementById("Edit");
        var input1 = document.createElement("input");
        var input2 = document.createElement("input");
        var input3 = document.createElement("input");
        var input4 = document.createElement("input");
        var input5 = document.createElement("input");





        var privacy_name = document.getElementById('privacy_name');
        var privacy_age = document.getElementById('privacy_age');
        var privacy_location = document.getElementById('privacy_location');
        var privacy_phnumber = document.getElementById('privacy_phnumber');
        var privacy_email = document.getElementById('privacy_email');

        input1.type = "text";
        input1.name ="name";
        input1.value=name;
        input2.type = "text";
        input2.name ="age";
        input2.value=age;
        input3.type = "text";
        input3.name ="location";
        input2.value =location;
        input4.type = "text";
        input4.name ="phnumber";
        input4.value = phnumber;
        input5.type = "text";
        input5.name ="email";
        input5.value = email;
        edit.parentNode.removeChild(edit);
        name.parentNode.replaceChild(input1,name); // put it into the DOM
        age.parentNode.replaceChild(input2,age); // put it into the DOM
        location.parentNode.replaceChild(input3,location); // put it into the DOM
        phnumber.parentNode.replaceChild(input4,phnumber); // put it into the DOM
        email.parentNode.replaceChild(input5,email); // put it into the DOM

        var s = document.createElement("input"); //input element, Submit button
        s.setAttribute('type',"submit");
        s.setAttribute('value',"Save");

        input5.parentNode.appendChild(s);

        if (n!='0'){
            privacy_name[0].defaultSelected=false;
            privacy_name[parseInt(n)].defaultSelected=true;
        }
        if (a!='0'){
            privacy_age[0].defaultSelected=false;
            privacy_age[parseInt(a)].defaultSelected=true;
        }
        if (l!='0'){
            privacy_location[0].defaultSelected=false;
            privacy_location[parseInt(l)].defaultSelected=true;

        }
        if (p!='0'){
            privacy_phnumber[0].defaultSelected=false;
            privacy_phnumber[parseInt(p)].defaultSelected=true;

        }
        if (e!='0'){
            privacy_email[0].defaultSelected=false;
            privacy_email[parseInt(e)].defaultSelected=true;

        }


        document.getElementById('privacy_name').style.visibility='visible';

        document.getElementById('privacy_age').style.visibility='visible';

        document.getElementById('privacy_location').style.visibility='visible';

        document.getElementById('privacy_phnumber').style.visibility='visible';

        document.getElementById('privacy_email').style.visibility='visible';



    }