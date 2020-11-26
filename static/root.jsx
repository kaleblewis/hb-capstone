const Router = ReactRouterDOM.BrowserRouter;
const Route =  ReactRouterDOM.Route;
const Link =  ReactRouterDOM.Link;
const Prompt =  ReactRouterDOM.Prompt;
const Switch = ReactRouterDOM.Switch;
const Redirect = ReactRouterDOM.Redirect;
const useParams = ReactRouterDOM.useParams;
const useHistory = ReactRouterDOM.useHistory;
// same as the above but using destructing syntax 
// const { useHistory, useParams, Redirect, Switch, Prompt, Link, Route } = ReactRouterDOM;

function Homepage() {
  return <div> Welcome to my site </div>
}

function About() {
  return <div> A tiny react demo site </div>
}

function SearchBar() { 
  return (
  <div>
      <input type="search"></input>
  </div>
  )
}

function Search() {
  return (
      <div>  
        Search for stuff 
        <SearchBar/>
      </div>
    )
}

function LogIn() { 

  const [email, setEmail] = React.useState('');
  const [password, setPassword] = React.useState('');

  function handleLogin(evt) {
    evt.preventDefault();
    // console.log((email)
    // console.log(password)
    
    const data = { 
      email: email,
      password: password
    }

    const options = {
      method: 'POST',
      body: JSON.stringify(data),
      headers: {
        'Content-Type': 'application/json'
      },
    }

    fetch('/api/login', options)
    .then(response => response.json())
    .then(data => {
      if (data === 'banana bunny muffins') {
        alert(data)
      } else{ 
        alert("no muffins, very sad")
      }
    })

  }

  function handleEmailChange(evt) {
    setEmail(evt.target.value)
  }

  function handlePasswordChange(evt) {
    // let what_they_just_typed = evt.target.value 
    // console.log(what_they_just_typed)
    setPassword(evt.target.value)
  }

  return (
    <div>
      <form onSubmit={handleLogin}>
        Username:
        <input value={email} onChange={handleEmailChange} type="text"></input>
        Password:
        <input value={password} onChange={handlePasswordChange} type="text"></input>
        <button>Login</button>
      </form>
    </div>
  )
}


function App() {
    return (
      <Router>
        <nav>
          <ul>
            <li>
                <Link to="/"> Home </Link>
            </li>

            <li>
                <Link to="/search"> Search </Link>
            </li>
            <li>
                <Link to="/profile"> Profile </Link>
            </li>
            <li>
                <Link to="/login"> Login </Link>
            </li>
          </ul>
        </nav>
        <div>
          <Switch>
            <Route path="/about">
              <About />
            </Route>
            <Route path="/login">
              <LogIn />
            </Route>
            <Route path="/profile">
              <Profile />
            </Route>
            <Route path="/search">
              <Search />
            </Route>
            <Route path="/recommendations">
              <Recommendations />
            </Route>
            <Route path="/title">
              <Title />
            </Route>
            <Route path="/actor">
              <Actor />
            </Route>
            <Route path="/">
              <Homepage />
            </Route>
          </Switch>
        </div>
      </Router>
    );
}

ReactDOM.render(<App />, document.getElementById('root'))

