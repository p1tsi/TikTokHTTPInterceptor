import { HTTPInterceptor_functions } from './HTTPInterceptor'


function attach_interceptor_to_func(func) {
    Interceptor.attach(
        func.ptr,
        {
            onEnter: function(args: InvocationArguments) {
                if (func.onEnter){
                    func.onEnter(args);
                }
            },
            onLeave: function(retval: NativePointer){
                if (func.onLeave){
                    func.onLeave(retval);
                }
            }
        }
    );
}


export function hook(modules: string[], customModules: string[]) {


    customModules.forEach(module => {
        if (module === 'HTTPInterceptor'){ HTTPInterceptor_functions.forEach(func => attach_interceptor_to_func(func))}
    });

    return true;
}