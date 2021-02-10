    var wbox = document.querySelector("#wbox");
    var obutton = document.querySelector("#obutton");
    var cbutton = document.querySelector("#cbutton");
    var wbutton = document.querySelector("#wbutton");
    var varName = document.querySelector("#name");
    var varSetValue = document.querySelector("#value");
    var varCurrentValue = document.querySelector("#currentvalue");
    var writeStatus = document.querySelector("#writestatus");

    obutton.onclick = togglewbox;
    cbutton.onclick = togglewbox;
    wbutton.onclick = writeToServer;

    setInterval(readVariablesAndFilterByName, 1000);
    



    function togglewbox(){
        if(wbox.style.display === "block") setTimeout(()=>{wbox.style.display = "none"}, 400);
        wbox.style.display = "block"
        toggleClass(wbox,"hide");
    }

    function toggleClass(element, cl){
        if( element.classList.contains(cl) ) element.classList.remove(cl);
        else element.classList.add(cl);
    }

    async function readVariablesAndFilterByName(){
        let resp = await fetch("variables");
        
        if( resp.status === 404 ) setValue("Var Not Found", true);
        else if(resp.status !== 200) setValue("Bad Request", true);
        else {
            var var_objs = {}
            try{
                var_objs = await resp.json();
                setValue( filter(varName.value,var_objs) );
            }
            catch{
                setValue("Bad Request", true);
            }
        }
        
    }

    function setValue(val, isError=false){
        varCurrentValue.innerText = val.toString();
        if(isError) varCurrentValue.style.color = "red";
        else varCurrentValue.style.color = "#606c76";
    }

    function setWriteStatus(val, isError=false){
        writeStatus.innerText = val.toString();
        if(isError) writeStatus.style.color = "red";
        else writeStatus.style.color = "green";
    }

    function filter(name, obj){
        if(Array.isArray(obj)){
            var requested_obj = obj.find((el)=>{return el.name === name; });
            if(requested_obj) return requested_obj.value.toString();
            else return "Not Found";
        }
        else return "Not Found";
    }

    async function writeToServer(){
        var data = {
            name  : varName.value,
            value : parseFloat(varSetValue.value)
        }

        let resp = await fetch("write",{
            method:"POST",
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });

        if( resp.status === 404 ) setWriteStatus("Var Not Found", true);
        else if(resp.status !== 200) setWriteStatus("Bad Request", true);
        else {
            var var_objs = {}
            try{
                var_objs = await resp.json();
                setWriteStatus("Success");
            }
            catch{
                setWriteStatus("Bad Request", true);
            }
        }
    }