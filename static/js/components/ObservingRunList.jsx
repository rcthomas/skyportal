import React from "react";
import { useSelector } from "react-redux";
import { Link } from "react-router-dom";
import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import ListItemText from "@material-ui/core/ListItemText";
import Typography from "@material-ui/core/Typography";
import { makeStyles } from "@material-ui/core/styles";
import PropTypes from "prop-types";
import { observingRunTitle } from "./AssignmentForm";

const useStyles = makeStyles((theme) => ({
  root: {
    width: "100%",
    maxWidth: "22.5rem",
    backgroundColor: theme.palette.background.paper,
  },
}));

const SimpleList = ({ observingRuns }) => {
  const classes = useStyles();
  const { instrumentList } = useSelector((state) => state.instruments);
  const { telescopeList } = useSelector((state) => state.telescopes);
  const groups = useSelector((state) => state.groups.all);

  return (
    <div className={classes.root}>
      <List component="nav">
        {observingRuns.map((run) => (
          <ListItem button component={Link} to={`/run/${run.id}`} key={run.id}>
            <ListItemText
              primary={observingRunTitle(
                run,
                instrumentList,
                telescopeList,
                groups
              )}
            />
          </ListItem>
        ))}
      </List>
    </div>
  );
};

const ObservingRunList = () => {
  const { observingRunList } = useSelector((state) => state.observingRuns);
  return (
    <div>
      <Typography variant="h6">List of Observing Runs</Typography>
      <SimpleList observingRuns={observingRunList} />
    </div>
  );
};

SimpleList.propTypes = {
  observingRuns: PropTypes.arrayOf(PropTypes.any).isRequired,
};

export default ObservingRunList;
