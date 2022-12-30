import AppContext from "context";
import { useContext, useEffect } from "react";
import { useNavigate } from "react-router-dom";

export default function LoginPage() {
  const {user, setBreadcrumbs} = useContext(AppContext);
  const navigate = useNavigate();

  useEffect(() => {
    if (user && user.id) {
      navigate('dashboard')
    }

    setBreadcrumbs([]);
  }, [user])
  
  return (
    <div className="mt-5 text-center">
      <a href={window.APP_URL + "/accounts/discord/login/"} className="text-white bg-blue-500 hover:bg-blue-600 font-medium rounded-lg text-sm px-5 py-2.5">
        Login with Discord
      </a>
    </div>
  );
}