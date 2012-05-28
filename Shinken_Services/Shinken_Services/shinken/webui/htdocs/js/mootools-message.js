/*
---
description: Message Class. A much more sophisticated way to alert your users.

license: MIT-style

authors:
- Jason Beaudoin
- ColdFire Designs

requires:
- core/1.3: '*'
- more/1.3.0.1:Array.Extras
- more/1.3.0.1:Chain.Wait
- more/1.3.0.1:Element.Position
- more/1.3.0.1:Element.Shortcuts
- more/1.3.0.1:Element.Measure

provides: [Message.say, Message.tell, Message.ask, Message.waiter, Message.tip]

...
*/

var Message=new Class({Implements:[Options,Events],msgChain:null,end:false,isDisplayed:false,windowSize:null,pageSize:null,page:$(document),box:null,boxSize:null,scrollPos:null,windowSize:null,hasVerticalBar:false,hasHorizontalBar:false,boxPos:function(){},tipCheck:true,cancel:false,fx:null,fxOut:null,options:{callingElement:null,top:false,left:false,centered:false,offset:30,width:"auto",icon:null,iconPath:"images/icons/",iconSize:40,fontSize:14,title:null,message:null,delay:0,autoDismiss:true,dismissOnEvent:false,isUrgent:false,callback:null,passEvent:null,stack:true,fxTransition:null,fxDuration:"normal",fxUrgentTransition:Fx.Transitions.Bounce.easeOut,fxOutTransition:null,fxOutDuration:"normal",yesLink:"Yes",noLink:"No"},initialize:function(a){this.setOptions(a);this.box=this;if(this.options.width=="auto"){this.options.width="250px"}if(this.options.passEvent!=null&&this.options.callingElement!=undefined){this.options.dismissOnEvent=true;this.options.callingElement.addEvent("mouseout",function(){if(this.isDisplayed){this.dismiss()}else{this.cancel=true}}.bind(this))}},say:function(d,c,b,a,e){this.setVars(d,c,b,a,e);this.box=this.createBox();this.msgChain=new Chain();this.setMsgChain()},ask:function(d,c,e,b,a){this.options.autoDismiss=false;if(e!=null){this.options.callback=e}a=a!=undefined?a:true;this.say(d,c,b,a,e)},tell:function(d,c,b,a){a=a!=undefined?a:true;this.options.dismissOnEvent=true;this.say(d,c,b,a)},waiter:function(d,c,b,a){if(a!=null){this.options.centered=a}this.options.autoDismiss=false;this.options.dismissOnEvent=true;this.options.centered=true;this.say(d,c,b)},tip:function(c,b,a){this.options.autoDismiss=true;this.options.dismissOnEvent=true;this.say(c,b,a)},setVars:function(d,c,b,a,e){if(d!=undefined){this.options.title=d}if(c!=undefined){this.options.message=c}if(b!=undefined){this.options.icon=b}if(a!=undefined){this.options.isUrgent=a}if(e!=undefined){this.options.callback=e}},setMsgChain:function(){if(this.fx==null){this.fx=new Fx.Tween(this.box,{link:"chain",onComplete:function(){if((this.options.autoDismiss&&!this.options.dismissOnEvent)||(!this.isDisplayed&&this.options.callback==null)){this.msgChain.callChain()}}.bind(this),transition:this.options.fxTransition,duration:this.options.fxDuration})}var a;if(this.options.callback!=null||this.options.autoDismiss==false||this.options.dismissOnEvent){a=0}else{a=2000}this.msgChain.wait(this.options.delay).chain(function(){if(!this.cancel){this.showMsg()}else{this.complete()}this.fireEvent("onShow")}.bind(this)).wait(a).chain(function(){this.hideMsg()}.bind(this)).callChain()},showMsg:function(){this.setSizes();this.setBoxPosition();if(this.hasVerticalBar){$(document.body).setStyle("overflow","hidden")}this.box.setStyles({opacity:0,top:this.boxPos.startTop,left:this.boxPos.startLeft,"z-index":"1"}).fade("in");if(!this.options.isUrgent){this.fx.start("top",this.boxPos.endTop)}else{var a=new Fx.Tween(this.box,{duration:"long",transition:this.options.fxUrgentTransition});a.start("top",this.boxPos.endTop)}this.isDisplayed=true},dismiss:function(){this.msgChain.callChain()},setBoxPosition:function(){this.boxPos={};var e=(this.options.top&&this.options.left),k,f,b,l,h=0,j=0,m=3.5,d,a=1,i,g=null,n;if(this.options.isUrgent){g="[class*=mcUrgent]"}else{if(this.options.top){g="[class*=mcTop]"}else{if(this.options.callingElement!=undefined){g="[class*=mcElement]"}else{g="[class*=mcDefault]"}}}if(this.options.stack){d=$$("[class*=messageClass]"+g+"");messagesInfo=d.getCoordinates();var i=new Array();var n=new Array();messagesInfo.each(function(o){i.push(o.height);if(o.top>0){n.push(o.top)}});h=this.scrollPos.y+this.windowSize.y-(i.sum()+m*d.length);if(h>=n.min()){h=n.min()-this.boxSize.y-m}j=i.sum()-this.boxSize.y+(m*d.length);if(n.length>0){if(j<=n[n.length-1]+i[i.length-2]+m){j=n[n.length-1]+i[i.length-2]+m}}}else{h=this.scrollPos.y+this.windowSize.y-this.boxSize.y-this.options.offset;j=this.options.offset}this.options.top?k=(this.boxSize.y*-1):k=this.scrollPos.y+this.windowSize.y;this.options.left?f=this.options.offset:f=this.windowSize.x-this.boxSize.x-this.options.offset;this.options.top?l=j:l=(h);if((this.options.passEvent!=null&&!this.options.isUrgent)&&!e){var c;(this.options.passEvent.page.x+this.boxSize.x>this.windowSize.x)?c=(this.boxSize.x*-1)-5:c=5;Object.append(this.boxPos,{startTop:this.options.passEvent.page.y-this.options.offset,startLeft:this.options.passEvent.page.x+c,endTop:this.options.passEvent.page.y+j-(m*3)})}else{if((this.options.isUrgent&&!e)||this.options.centered){this.box.position();this.boxPosition=this.box.getCoordinates();if(this.options.stack&&d.length>1){j=n[n.length-1]+i[i.length-2]+m}else{j=this.boxPosition.top}Object.append(this.boxPos,{startTop:this.boxPosition.top-100,startLeft:this.boxPosition.left,endTop:j})}else{Object.append(this.boxPos,{startTop:k,startLeft:f,endTop:l})}}},setSizes:function(){this.boxSize=this.box.getSize();this.boxPosition=this.box.getCoordinates();this.windowSize=this.page.getSize();this.scrollPos=this.page.getScroll();this.pageSize=this.page.getScrollSize();if(this.windowSize.y>=this.pageSize.y){this.hasVerticalBar=true||false}if(this.windowSize.x>=this.pageSize.x){this.hasHorizontalBar=true||false}},createBox:function(){var l="",c="",u="",t="",j="",v,g,o,q,s,h,m,a,k;if(this.options.top){l=" mcTop"}else{if(this.options.isUrgent){t=" mcUrgent"}else{if(this.options.callingElement!=undefined){j=" mcElement"}else{u=" mcDefault"}}}newBox=new Element("div",{"class":"msgBox messageClass"+l+u+t+j,styles:{"max-width":this.options.width,width:this.options.width}});g=0;if(this.options.icon!=null){var e=new Element("div",{"class":"msgBoxIcon"});var f=new Element("img",{"class":"msgBoxImage",src:this.options.iconPath+this.options.icon,styles:{width:this.options.iconSize,height:this.options.iconSize}})}if(this.options.title==null||this.options.message==null){this.getContent()}o=new Element("div",{"class":"msgBoxContent"}).setStyle("font-size",this.options.fontSize);q=new Element("div",{"class":"msgBoxTitle",html:this.options.title}).setStyle("font-size",this.options.fontSize+4);imageWidth=this.getCSSTotalWidth("msgBoxIcon");h=new Element("div",{"class":"clear"});m=new Element("div",{html:this.options.message+"<br />",styles:{margin:"0px",width:this.options.width.toInt()-imageWidth}});a=this.options.message.indexOf("textarea")>-1;if(this.options.callback!=null&&!a){var r=this.createLink(this.options.yesLink,true);var b=this.createLink(this.options.noLink,false);r.inject(m);m.appendText(" | ");b.inject(m)}else{if(a){var n=this.createLink("Send",true);var d=this.createLink("Cancel",false);n.inject(m);m.appendText(" | ");d.inject(m)}else{if(this.options.isUrgent||(!this.options.autoDismiss&&!this.options.dismissOnEvent)){var i=this.createLink("Ok",false);i.inject(m)}}}k=new Element("div",{"class":"msgBoxMessage"});m.inject(k);if(this.options.icon!=null){e.inject(newBox);f.inject(e)}o.inject(newBox);q.inject(o);h.inject(o);k.inject(o);newBox.inject(this.page.body);this.box=newBox;return newBox},createLink:function(b,a){var c=new Element("a",{href:"javascript:","class":"msgBoxLink",html:b,id:b.replace(" ","_")+"Link",events:{click:function(){this.msgChain.callChain();if(a){this.executeCallback()}}.bind(this)}});return c},getCSSTotalWidth:function(b){var c=new Element("div",{id:"dummy","class":b});c.inject($(document.body));var a=c.getComputedSize();c.dispose();return a.totalWidth},executeCallback:/* Added by Jean for input get */
		       function(){
			   var formValue = null;
			   var inputField = this.box.getElement('input');
			   /*alert('input'+inputField);*/
			   var textArea = this.box.getElement('textarea');
			   /*alert('text aera'+textArea);*/
			   if(inputField || textArea) {
			       formValue = (inputField ? inputField.get("value") :
					    (textArea ? textArea.get("value") : null));
			   }
			   /*alert(formValue == null);*/
			   if(typeOf(this.options.callback)=="element"){
			       this.options.callback.fireEvent("click", formValue)}
			   else{
			       if(typeOf(this.options.callback)=="function"){
				   /*alert('raise function'+formValue);*/
				   this.options.callback.run(formValue)
			       }else{
				   eval(this.options.callback)}}}
		       ,getContent:function(){var d;var c;if(this.options.callingElement!=undefined){var b=this.options.callingElement.getProperty("rel");var a;if(b==null){a=this.setError("Expected data in the 'rel' property of this calling element was not defined.");d=a[0];c=a[1];this.options.autoDismiss=false}else{a=b.split("::");d=a[0];c=a[1]}}this.options.title=d;this.options.message=c},setError:function(b){var a=new Array();a.push("<span style='color:#FF0000'>Error!</span>");a.push(b);return a},complete:function(){this.box.dispose();this.end=true;this.isDisplayed=false;this.fireEvent("onComplete");$(document.body).setStyle("overflow","auto")},hideMsg:function(){if(this.hasVerticalBar){$(document.body).setStyle("overflow","hidden")}var a=this.box.getCoordinates();this.box.fade("out");this.fxOut=new Fx.Tween(this.box,{transition:this.options.fxOutTransition,duration:this.options.fxOutDuration});this.fxOut.addEvent("complete",function(){this.complete()}.bind(this));var b;this.options.top?b=this.boxSize.y*-1:b=a.top+this.boxSize.y;this.fxOut.start("top",b)}});