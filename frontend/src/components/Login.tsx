import { useNavigate } from "react-router";

function Login() {
  const navigate = useNavigate();

  const submit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    //get the username and password
    const username = (
      document.getElementById("username-input") as HTMLInputElement
    ).value;
    const password = (
      document.getElementById("password-input") as HTMLInputElement
    ).value;

    fetch("/api/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username,
        password,
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.message === "Login successful") {
          navigate("/machines");
        } else {
          console.log(data.message);
        }
      })
      .catch((err) => {
        console.log("BIG ERROR: ", err);
      });
  };

  return (
    <div className="flex flex-col items-center justify-center mt-52">
      <h1 className="font-extrabold text-5xl">Login</h1>
      <form
        onSubmit={submit}
        id="login-form"
        className="flex flex-col mx-6 mt-8 gap-3"
      >
        <input
          type="text"
          placeholder="Username"
          id="username-input"
          className="bg-slate-200 outline-4 outline-black rounded-lg p-2"
        />
        <input
          type="password"
          placeholder="Password"
          id="password-input"
          className="bg-slate-200 outline-4 outline-black rounded-lg p-2"
        />
        <button
          type="submit"
          className="bg-black text-white p-3 w-full font-bold rounded-xl"
        >
          Login
        </button>
      </form>
    </div>
  );
}

export default Login;
