interface IFunctionPointer {
    name: string,
    ptr: NativePointer,
    onEnter?,
    onLeave?,
}

function ObjCObjectTOJSONString(object: NativePointer){
    let msgData = ObjC.classes.NSJSONSerialization.dataWithJSONObject_options_error_(object, 0, ptr('0x0'));
    let msgString = ObjC.classes.NSString.alloc()
    msgString = msgString.initWithData_encoding_(msgData, 4);
    return msgString.toString();
}


const TTHttpTaskChromium_resume: IFunctionPointer = {
    name: '-[TTHttpTaskChromium resume]',
    ptr: ObjC.classes.TTHttpTaskChromium['- resume'].implementation,
    onEnter: function(args: InvocationArguments){
        this.request = new ObjC.Object(args[0]).request();
        let body = this.request.body();
        if (body){
            send({
                type: 'HTTPInterceptor',
                timestamp: Date.now(),
                symbol: this.name,
                tid: this.threadId,
                data: {
                    args: [
                        this.request.urlString().toString(),
                        this.request.HTTPMethod().toString(),
                        ObjCObjectTOJSONString(this.request.allHTTPHeaders()),
                    ]
                }
            }, body.bytes().readByteArray(body.length()));
        }
        else{
            send({
                type: 'HTTPInterceptor',
                timestamp: Date.now(),
                symbol: this.name,
                tid: this.threadId,
                data: {
                    args: [
                        this.request.urlString().toString(),
                        this.request.HTTPMethod().toString(),
                        ObjCObjectTOJSONString(this.request.allHTTPHeaders()),
                    ]
                }
            });
        }
    }
}

const AWEJSONResponseSerializer_responseObjectForResponse_jsonObj_responseError_resultError_: IFunctionPointer = {
    name: '-[AWEJSONResponseSerializer responseObjectForResponse:jsonObj:responseError:resultError:]',
    ptr: ObjC.classes.AWEJSONResponseSerializer['- responseObjectForResponse:jsonObj:responseError:resultError:'].implementation,
    onEnter: function(args: InvocationArguments){
        this.response = new ObjC.Object(args[2]);
    },
    onLeave: function(retval: NativePointer){
        if (retval){
            send({
                type: 'HTTPInterceptor',
                timestamp: Date.now(),
                symbol: this.name,
                tid: this.threadId,
                data: {
                    args: [
                        this.response.httpURL().toString(),
                        this.response.httpStatusCode().toString(),
                        ObjCObjectTOJSONString(this.response.allHeaders())
                    ],
                    ret: ObjCObjectTOJSONString(retval)
                }
            })
        }
        else{
            send({
                type: 'HTTPInterceptor',
                timestamp: Date.now(),
                symbol: this.name,
                tid: this.threadId,
                data: {
                    args: [
                        this.response.httpURL().toString(),
                        this.response.httpStatusCode().toString(),
                        ObjCObjectTOJSONString(this.response.allHeaders())
                    ],
                }
            })
        }
    }
}


const AWEBinaryResponseSerializer_responseObjectForResponse_data_responseError_resultError_: IFunctionPointer = {
    name: '-[AWEBinaryResponseSerializer responseObjectForResponse:data:responseError:resultError:]',
    ptr: ObjC.classes.AWEBinaryResponseSerializer['- responseObjectForResponse:data:responseError:resultError:'].implementation,
    onEnter: function(args: InvocationArguments){
        this.response = new ObjC.Object(args[2]);
    },
    onLeave: function(retval: NativePointer){
        if (!retval.isNull()){
            let data = new ObjC.Object(retval);
            send({
                type: 'HTTPInterceptor',
                timestamp: Date.now(),
                symbol: this.name,
                tid: this.threadId,
                data: {
                    args: [
                        this.response.httpURL().toString(),
                        this.response.httpStatusCode().toString(),
                        ObjCObjectTOJSONString(this.response.allHeaders())
                    ],
                }
            }, data.bytes().readByteArray(data.length()))
        }
        else{
            send({
                type: 'HTTPInterceptor',
                timestamp: Date.now(),
                symbol: this.name,
                tid: this.threadId,
                data: {
                    args: [
                        this.response.httpURL().toString(),
                        this.response.httpStatusCode().toString(),
                        ObjCObjectTOJSONString(this.response.allHeaders())
                    ],
                }
            })
        }
    }
}


export const HTTPInterceptor_functions = [
    TTHttpTaskChromium_resume,
    AWEJSONResponseSerializer_responseObjectForResponse_jsonObj_responseError_resultError_,
    AWEBinaryResponseSerializer_responseObjectForResponse_data_responseError_resultError_
]