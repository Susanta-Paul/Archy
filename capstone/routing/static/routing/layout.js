let bars=document.querySelector("#lines");
let sidebar=document.querySelector(".sidebar");


bars.addEventListener("click", ()=>{
  if(sidebar.style.display==="none"){
    sidebar.style.display="inline";
  }else{
    sidebar.style.display="none";
  }
});

let search=document.querySelector("#pp");
let open=document.querySelector(".modal");
let cancel=document.querySelector("#cancel");

search.addEventListener("click", ()=>{
  open.showModal();
})
cancel.addEventListener("click",()=>{
  open.close();
})


let pencil1=document.querySelector("#pencil1");
let modalInfo=document.querySelector(".modalInfo");

let cancel1=document.querySelector("#cancel1");

pencil1.addEventListener("click",()=>{
    modalInfo.showModal();
});

cancel1.addEventListener("click", ()=>{
    modalInfo.close();
})

let pencil2=document.querySelector("#pencil2");
let modalAbout=document.querySelector(".modalAbout");
let cancel2=document.querySelector("#cancel2");

pencil2.addEventListener("click",()=>{
    modalAbout.showModal();
});
cancel2.addEventListener("click", ()=>{
    modalAbout.close();
})

let pencil3=document.querySelector("#pencil3");
let modalWork=document.querySelector(".modalWork");
let cancel3=document.querySelector("#cancel3");
pencil3.addEventListener("click",()=>{
    modalWork.showModal();
});
cancel3.addEventListener("click", ()=>{
    modalWork.close();
})

images=document.querySelector(".photos");
photos=document.querySelector(".zoom");


if(images.length==1){
  photos.showModal()
  console.log("success!");
}else{
  for(let i=0; i<images.length; i++){
  images[i].addEventListener("click",()=>{
    photos[i].showMOdal();
    console.log("success!");
  });
};
};
