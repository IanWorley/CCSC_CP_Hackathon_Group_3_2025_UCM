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
import { Select, SelectContent, SelectItem } from "@/components/ui/select";
import { BuildingDictionary } from "@/model/BuildingList";
import { zodResolver } from "@hookform/resolvers/zod";
import { SelectTrigger } from "@radix-ui/react-select";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { Link, useNavigate } from "react-router";
import { z } from "zod";

function Register() {
  const navigate = useNavigate();

  const [backendRegisterStatus, setBackendRegisterStatus] = useState(false);

  const formSchema = z.object({
    username: z.string().min(3, {
      message: "Username must be at least 2 characters.",
    }),
    password: z.string().min(8, {
      message: "Password must be at least 8 characters.",
    }),
    studentEmail: z
      .string()
      .email({
        message: "Invalid email address",
      })
      .regex(/@ucmo\.edu$/),

    studentId: z.string().regex(/^\d{9}\d?$/, {
      message: "Student ID must be 9 digits",
    }),
    buildingId: z.enum(
      Array.from(BuildingDictionary.keys()).map(String) as [
        string,
        ...string[],
      ],
      {
        message: "Please select a building",
      }
    ),
  });

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      username: "",
      password: "",
      studentEmail: "",
      studentId: "",
      buildingId: undefined,
    },
  });

  async function onSubmit(values: z.infer<typeof formSchema>) {
    const res = await fetch("/api/register", {
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
      setBackendRegisterStatus(true);
      console.error(res);
    }
  }

  return (
    <div className="mx-auto p-2 ">
      <h1 className="text-lg text-center font-bold">Register</h1>
      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className=" p-4 ">
          <FormField
            control={form.control}
            name="studentEmail"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Student Email</FormLabel>
                <FormControl>
                  <Input type="email" placeholder="Student Email" {...field} />
                </FormControl>
                <FormDescription>This is your student email.</FormDescription>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="studentId"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Student ID</FormLabel>
                <FormControl>
                  <Input placeholder="Student ID" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="buildingId"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Building</FormLabel>
                <Select
                  onValueChange={(value) => {
                    field.onChange(value);
                  }}
                >
                  <FormControl>
                    <SelectTrigger className="w-[180px]">
                      {BuildingDictionary.get(Number(field.value)) ??
                        "Select a building"}
                    </SelectTrigger>
                  </FormControl>
                  <SelectContent>
                    {Array.from(BuildingDictionary.entries()).map(
                      ([key, value]) => (
                        <SelectItem
                          className="h-[25px] md:h-auto"
                          key={key}
                          value={key.toString()}
                          onClick={() => field.onChange(key)}
                        >
                          {value}
                        </SelectItem>
                      )
                    )}
                  </SelectContent>
                </Select>

                <FormMessage />
              </FormItem>
            )}
          />

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
            render={({ field }) => (
              <FormItem>
                <FormLabel>Password</FormLabel>
                <FormControl>
                  <Input type="password" placeholder="Password" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          {backendRegisterStatus ? (
            <p className="text-center text-red-600">Something went wrong.</p>
          ) : null}

          <Link to="/login" className="text-sm text-blue-500 underline ">
            <p className="text-center ">Already have an account? Login </p>
          </Link>

          <Button className=" flex mx-auto w-3/4 mt-5" type="submit">
            Submit
          </Button>
        </form>
      </Form>
    </div>
  );
}

export default Register;
