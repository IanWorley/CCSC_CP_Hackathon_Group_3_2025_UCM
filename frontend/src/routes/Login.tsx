import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { zodResolver } from "@hookform/resolvers/zod";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router";
import { z } from "zod";

function Login() {
  const navigate = useNavigate();

  const [backendLoginStatus, setBackendLoginStatus] = useState(false);

  const formSchema = z.object({
    username: z.string().min(3, {
      message: "Username must be at least 2 characters.",
    }),
    password: z.string().min(8, {
      message: "Password must be at least 8 characters.",
    }),
  });

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      username: "",
      password: "",
    },
  });

  async function onSubmit(values: z.infer<typeof formSchema>) {
    const res = await fetch("/api/login", {
      method: "POST",
      body: JSON.stringify(values),
      headers: {
        "Content-Type": "application/json",
      },
    });

    form.reset();

    if (res.ok) {
      navigate("/");
    } else {
      console.error("Error logging in" + res.json());
      setBackendLoginStatus(true);
    }
  }

  return (
    <div className="mx-auto p-2 ">
      <h1 className="text-lg text-center font-bold">Login</h1>
      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className=" p-4 ">
          <FormField
            control={form.control}
            name="username"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Username</FormLabel>
                <FormControl>
                  <Input placeholder="Username" {...field} />
                </FormControl>
                <FormDescription>
                  This is your public display name.
                </FormDescription>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="password"
            render={({ field }) => {
              return (
                <FormItem>
                  <FormLabel>Password</FormLabel>
                  <FormControl>
                    <Input type="password" placeholder="Password" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              );
            }}
          />

          {backendLoginStatus ? (
            <p className="text-center text-red-600 my-2">
              Sorry, we don't recognize the login.
            </p>
          ) : null}

          <Button className="  flex mx-auto w-3/4 mt-5" type="submit">
            Submit
          </Button>
        </form>
      </Form>
    </div>
  );
}

export default Login;
